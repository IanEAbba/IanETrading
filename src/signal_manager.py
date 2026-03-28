"""SignalManager — Strategy evaluation engine.

Loads enabled strategy plugins from config, evaluates each ticker's
market data through each strategy, and returns aggregated signals.
"""

import logging

import pandas as pd

from src.strategies.base import BaseStrategy, Signal
from src.strategies.momentum import MomentumStrategy

logger = logging.getLogger(__name__)

# Registry mapping config strategy names to their classes.
# To add a new strategy: import it and add an entry here.
_STRATEGY_REGISTRY: dict[str, type[BaseStrategy]] = {
    "momentum": MomentumStrategy,
}


class SignalManager:
    """Loads strategy plugins and evaluates market data to produce trading signals.

    Reads config["strategies"] to determine which strategies are enabled,
    instantiates each with its configuration, and runs them against provided data.

    Args:
        config: Full config dict from load_config().
    """

    def __init__(self, config: dict):
        self._strategies: list[BaseStrategy] = []
        strategies_cfg = config.get("strategies", {})

        for name, strategy_cfg in strategies_cfg.items():
            if not isinstance(strategy_cfg, dict):
                logger.warning("Invalid config for strategy '%s', skipping", name)
                continue

            if not strategy_cfg.get("enabled", False):
                logger.debug("Strategy '%s' is disabled, skipping", name)
                continue

            cls = _STRATEGY_REGISTRY.get(name)
            if cls is None:
                logger.warning(
                    "Unknown strategy '%s' in config — not in registry. Skipping.", name
                )
                continue

            # Pass strategy-specific config (without the 'enabled' key)
            params = {k: v for k, v in strategy_cfg.items() if k != "enabled"}
            self._strategies.append(cls(params))
            logger.info("Loaded strategy: %s", name)

    @property
    def strategy_names(self) -> list[str]:
        """Names of loaded (enabled) strategies."""
        return [s.name for s in self._strategies]

    def evaluate_all(self, data: dict[str, pd.DataFrame]) -> list[Signal]:
        """Run all enabled strategies against all tickers.

        Args:
            data: Dict mapping ticker → OHLCV DataFrame, as returned by
                DataFetcher.fetch_multiple().

        Returns:
            List of Signal objects — one per (ticker, strategy) pair.
            Includes hold signals for full visibility. TradeExecutor
            should filter for actionable signals (buy/sell).
        """
        signals: list[Signal] = []

        for ticker, df in data.items():
            for strategy in self._strategies:
                try:
                    signal = strategy.evaluate(ticker, df)
                    signals.append(signal)
                except Exception:
                    logger.exception(
                        "[%s] Strategy '%s' raised an exception", ticker, strategy.name
                    )
                    signals.append(Signal(
                        ticker=ticker,
                        action="hold",
                        strength=0.0,
                        reason=f"Strategy '{strategy.name}' failed with an error",
                    ))

        logger.info(
            "Evaluated %d ticker(s) × %d strategy(ies) → %d signal(s)",
            len(data),
            len(self._strategies),
            len(signals),
        )
        return signals
