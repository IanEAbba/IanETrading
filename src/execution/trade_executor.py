import os
import logging
from datetime import datetime
from typing import List
from ..core.models import Signal, OrderIntent
from ..core.state_store import StateStore


logger = logging.getLogger(__name__)


class TradeExecutor:
    def __init__(self):
        self.simulate = os.getenv("SIMULATE", "1") == "1"
        self.base_qty = 1.0 # simple fixed size; replace with risk-based sizing


    def plan(self, sig: Signal, state: StateStore) -> List[OrderIntent]:
        side = "buy" if sig.action == "BUY" else ("sell" if sig.action == "SELL" else None)
        if not side:
            return []
        cid = f"IANE-{sig.symbol}-{int(sig.ts.timestamp())}"
        return [OrderIntent(symbol=sig.symbol, side=side, qty=self.base_qty, ts=sig.ts, client_id=cid)]


    async def execute(self, intents: List[OrderIntent], state: StateStore):
        if not intents:
            return
        if self.simulate:
            for it in intents:
                logger.info(f"SIM ORDER {it.side.upper()} {it.qty} {it.symbol} @ {it.ts} cid={it.client_id}")
                state.add_order(it.symbol, it.side, it.qty, it.client_id or "", it.ts, status="simulated")
            return
        # Live paper via Alpaca REST
        from alpaca.trading.client import TradingClient
        from alpaca.trading.requests import MarketOrderRequest
        from alpaca.trading.enums import OrderSide, TimeInForce


        key = os.getenv("ALPACA_API_KEY_ID"); sec = os.getenv("ALPACA_API_SECRET_KEY")
        base_url = os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")
        client = TradingClient(key, sec, paper=True)


        for it in intents:
            try:
                req = MarketOrderRequest(
                    symbol=it.symbol,
                    qty=it.qty,
                    side=OrderSide.BUY if it.side=="buy" else OrderSide.SELL,
                    time_in_force=TimeInForce.DAY,
                    client_order_id=it.client_id
                )
                order = client.submit_order(req)
                logger.info(f"LIVE ORDER {it.side.upper()} {it.qty} {it.symbol} id={order.id}")
                state.add_order(it.symbol, it.side, it.qty, it.client_id or "", it.ts, status="submitted")
            except Exception as e:
                logger.error(f"Order failed for {it.symbol}: {e}")