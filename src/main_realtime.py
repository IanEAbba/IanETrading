import os
import asyncio
import logging
from dotenv import load_dotenv
from src.core.logging_setup import setup_logging
from src.core.event_bus import EventBus
from src.core.state_store import StateStore
from src.ingest.realtime_ingestor import RealtimeIngestor
from src.processing.bar_aggregator import BarAggregator
from src.processing.strategy_engine import StrategyEngine
from src.execution.risk_manager import RiskManager
from src.execution.trade_executor import TradeExecutor
# from src.observability.monitor_api import run_monitor_api


logger = logging.getLogger(__name__)


async def processor_loop(bus, aggregator, strategy, risk, executor, state):
    while True:
        ev = await bus.consume()
        bars = aggregator.on_event(ev)
        for bar in bars:
            sig = strategy.on_bar(bar)
            if not sig:
                continue
            state.add_signal(sig.symbol, sig.action, sig.confidence, sig.reason, sig.ts)
            ok, reason = risk.validate(sig, state)
            if not ok:
                logger.info(f"Signal blocked by risk: {reason}")
                continue
            intents = executor.plan(sig, state)
            await executor.execute(intents, state)


async def main():
    load_dotenv()
    setup_logging()
    logger.info("Starting IanETrading realtime loop…")


    symbols = os.getenv("SYMBOLS", "AAPL").split(",")
    bus = EventBus()
    state = StateStore("state.db")
    ingestor = RealtimeIngestor(bus, symbols)
    aggregator = BarAggregator(timeframe=os.getenv("TIMEFRAME", "1m"))
    strategy = StrategyEngine()
    risk = RiskManager()
    executor = TradeExecutor()


    tasks = [
        asyncio.create_task(ingestor.run()),
        asyncio.create_task(processor_loop(bus, aggregator, strategy, risk, executor, state)),
        # asyncio.create_task(asyncio.to_thread(run_monitor_api)),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down…")