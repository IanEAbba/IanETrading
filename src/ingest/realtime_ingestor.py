import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List
from ..core.event_bus import EventBus
from ..core.models import Tick


logger = logging.getLogger(__name__)


class RealtimeIngestor:
    def __init__(self, bus: EventBus, symbols: List[str]):
        self.bus = bus
        self.symbols = symbols
        self.simulate = os.getenv("SIMULATE", "1") == "1"


    async def run(self):
        if self.simulate:
            await self._run_simulated()
        else:
            await self._run_alpaca()


    async def _run_simulated(self):
        logger.info("RealtimeIngestor running in SIMULATION mode")
        price = {s: 100.0 for s in self.symbols}
        while True:
            now = datetime.utcnow()
            for s in self.symbols:
        # tiny random-walk without importing random
                millis = now.microsecond // 1000
                delta = ((millis % 7) - 3) * 0.01
                price[s] = max(1.0, price[s] + delta)
                await self.bus.publish(Tick(symbol=s, ts=now, price=price[s], size=1))
            await asyncio.sleep(0.2)


    async def _run_alpaca(self):
        logger.info("RealtimeIngestor connecting to Alpaca WS...")
        # Lazy import so SIMULATE doesn’t require alpaca-py
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.live import StockDataStream
        from alpaca.data.timeframe import TimeFrame


        key = os.getenv("ALPACA_API_KEY_ID"); sec = os.getenv("ALPACA_API_SECRET_KEY")
        feed = os.getenv("ALPACA_DATA_FEED", "iex")
        stream = StockDataStream(key, sec, raw_data=True, feed=feed)


        async def on_bar(bar):
        # If you want per-bar ingestion instead of ticks, you can publish here
        # This scaffold uses ticks synthesized from bar close
            tick = Tick(symbol=bar.get("S"), ts=datetime.fromtimestamp(bar.get("t")/1e9), price=bar.get("c"), size=bar.get("v", 1))
            await self.bus.publish(tick)


        async def on_trade(trade):
            tick = Tick(symbol=trade.get("S"), ts=datetime.fromtimestamp(trade.get("t")/1e9), price=trade.get("p"), size=trade.get("s", 1))
            await self.bus.publish(tick)


        for s in self.symbols:
            stream.subscribe_trades(on_trade, s)
            # Optionally also bars: stream.subscribe_bars(on_bar, s)


        while True:
            try:
                await stream._run_forever() # internal run loop; reconnects handled by alpaca-py
            except Exception as e:
                logger.error(f"WS error {e}; retrying in 5s")
                await asyncio.sleep(5)