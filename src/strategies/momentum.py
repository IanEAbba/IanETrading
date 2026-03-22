"""Smart Money Momentum strategy.

Detects institutional buying behavior through unusual volume spikes
combined with price breakouts. Migrated and improved from legacy app/strategy.py.
"""

import logging

import pandas as pd

from src.strategies.base import BaseStrategy, Signal

logger = logging.getLogger(__name__)


class MomentumStrategy(BaseStrategy):
    """Smart Money Momentum detection strategy.

    Triggers a buy signal when:
    - Price change exceeds the configured threshold (default: 1.0%)
    - Latest volume exceeds average volume by the configured multiplier (default: 2.0x)
    """

    @property
    def name(self) -> str:
        return "momentum"

    def evaluate(self, ticker: str, df: pd.DataFrame) -> Signal:
        """Evaluate ticker for momentum signal.

        Args:
            ticker: Stock symbol.
            df: OHLCV DataFrame.

        Returns:
            Signal with buy/hold action.
        """
        price_threshold = self.config.get("price_threshold", 1.0)
        volume_multiplier = self.config.get("volume_multiplier", 2.0)

        # Validate input
        required_columns = {"open", "close", "volume"}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            return Signal(
                ticker=ticker,
                action="hold",
                strength=0.0,
                reason=f"Missing required columns: {missing}",
            )

        if len(df) < 2:
            return Signal(
                ticker=ticker,
                action="hold",
                strength=0.0,
                reason="Not enough data to evaluate (need at least 2 bars)",
            )

        # Calculate metrics
        open_price = df["open"].iloc[0]
        if open_price == 0:
            return Signal(
                ticker=ticker,
                action="hold",
                strength=0.0,
                reason="Open price is zero — cannot calculate change",
            )

        close_price = df["close"].iloc[-1]
        price_change = (close_price - open_price) / open_price * 100
        avg_volume = df["volume"].mean()
        last_volume = df["volume"].iloc[-1]

        volume_ratio = last_volume / avg_volume if avg_volume > 0 else 0.0

        # Check conditions
        price_ok = price_change >= price_threshold
        volume_ok = volume_ratio >= volume_multiplier

        if price_ok and volume_ok:
            strength = min(1.0, (price_change / price_threshold) * 0.5
                           + (volume_ratio / volume_multiplier) * 0.5)
            reason = (
                f"Momentum detected: price +{price_change:.2f}% "
                f"(threshold: {price_threshold}%), "
                f"volume {volume_ratio:.1f}x avg (threshold: {volume_multiplier}x)"
            )
            logger.info("[%s] BUY signal — %s", ticker, reason)
            return Signal(ticker=ticker, action="buy", strength=strength, reason=reason)

        reason = (
            f"No signal: price +{price_change:.2f}% "
            f"({'OK' if price_ok else 'below threshold'}), "
            f"volume {volume_ratio:.1f}x avg "
            f"({'OK' if volume_ok else 'below threshold'})"
        )
        logger.debug("[%s] HOLD — %s", ticker, reason)
        return Signal(ticker=ticker, action="hold", strength=0.0, reason=reason)
