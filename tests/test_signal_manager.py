"""Tests for the SignalManager module."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from src.signal_manager import SignalManager


def _make_config(strategies: dict | None = None) -> dict:
    """Build a minimal config with given strategies section."""
    if strategies is None:
        strategies = {
            "momentum": {
                "enabled": True,
                "price_threshold": 1.0,
                "volume_multiplier": 2.0,
            }
        }
    return {"strategies": strategies}


class TestSignalManagerLoading:

    def test_loads_enabled_strategies(self):
        mgr = SignalManager(_make_config())
        assert mgr.strategy_names == ["momentum"]

    def test_skips_disabled_strategies(self):
        config = _make_config({
            "momentum": {
                "enabled": False,
                "price_threshold": 1.0,
                "volume_multiplier": 2.0,
            }
        })
        mgr = SignalManager(config)
        assert mgr.strategy_names == []

    def test_unknown_strategy_skipped(self):
        config = _make_config({
            "nonexistent_strategy": {
                "enabled": True,
            }
        })
        mgr = SignalManager(config)
        assert mgr.strategy_names == []

    def test_no_strategies_enabled_returns_empty(self):
        mgr = SignalManager(_make_config({}))
        signals = mgr.evaluate_all({"AAPL": pd.DataFrame()})
        assert signals == []

    def test_strategy_names_property(self):
        mgr = SignalManager(_make_config())
        assert isinstance(mgr.strategy_names, list)
        assert "momentum" in mgr.strategy_names


class TestSignalManagerEvaluate:

    def test_evaluate_all_returns_signals_for_each_ticker(self, sample_ohlcv_bullish):
        mgr = SignalManager(_make_config())
        data = {"AAPL": sample_ohlcv_bullish, "MSFT": sample_ohlcv_bullish}
        signals = mgr.evaluate_all(data)

        assert len(signals) == 2
        tickers = {s.ticker for s in signals}
        assert tickers == {"AAPL", "MSFT"}

    def test_evaluate_all_buy_signal_on_bullish_data(self, sample_ohlcv_bullish):
        mgr = SignalManager(_make_config())
        signals = mgr.evaluate_all({"AAPL": sample_ohlcv_bullish})

        assert len(signals) == 1
        assert signals[0].action == "buy"
        assert signals[0].ticker == "AAPL"
        assert signals[0].strength > 0.0

    def test_evaluate_all_hold_on_flat_data(self, sample_ohlcv_flat):
        mgr = SignalManager(_make_config())
        signals = mgr.evaluate_all({"AAPL": sample_ohlcv_flat})

        assert len(signals) == 1
        assert signals[0].action == "hold"

    def test_evaluate_all_with_empty_data(self, sample_ohlcv_empty):
        mgr = SignalManager(_make_config())
        signals = mgr.evaluate_all({"AAPL": sample_ohlcv_empty})

        assert len(signals) == 1
        assert signals[0].action == "hold"
        assert "Not enough data" in signals[0].reason

    def test_strategy_exception_returns_hold(self, sample_ohlcv_bullish):
        """If a strategy's evaluate() raises, return a hold signal instead of crashing."""
        mgr = SignalManager(_make_config())

        # Patch the loaded strategy's evaluate to raise
        mgr._strategies[0].evaluate = MagicMock(side_effect=RuntimeError("boom"))

        signals = mgr.evaluate_all({"AAPL": sample_ohlcv_bullish})

        assert len(signals) == 1
        assert signals[0].action == "hold"
        assert "failed" in signals[0].reason.lower()
