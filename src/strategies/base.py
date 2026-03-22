"""Base strategy interface for IanETrading.

All trading strategies must inherit from BaseStrategy and implement the evaluate() method.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd


@dataclass
class Signal:
    """Trading signal produced by a strategy.

    Attributes:
        ticker: Stock symbol.
        action: Trade action — "buy", "sell", or "hold".
        strength: Signal confidence from 0.0 (weak) to 1.0 (strong).
        reason: Human-readable explanation of why the signal was generated.
    """

    ticker: str
    action: str  # "buy", "sell", "hold"
    strength: float  # 0.0 to 1.0
    reason: str


class BaseStrategy(ABC):
    """Abstract base class for trading strategies.

    Subclasses must implement evaluate() to analyze market data and return a Signal.

    Args:
        config: Strategy-specific configuration dictionary.
    """

    def __init__(self, config: dict):
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique strategy identifier."""
        ...

    @abstractmethod
    def evaluate(self, ticker: str, df: pd.DataFrame) -> Signal:
        """Evaluate market data and produce a trading signal.

        Args:
            ticker: Stock symbol being evaluated.
            df: OHLCV DataFrame with columns: open, high, low, close, volume.

        Returns:
            Signal with action, strength, and reason.
        """
        ...
