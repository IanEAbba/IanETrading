"""Tests for the Smart Money Momentum strategy."""

import pandas as pd

from src.strategies.momentum import MomentumStrategy


def _make_strategy(price_threshold=1.0, volume_multiplier=2.0):
    return MomentumStrategy({
        "price_threshold": price_threshold,
        "volume_multiplier": volume_multiplier,
    })


class TestMomentumStrategy:

    def test_buy_signal_on_bullish_data(self, sample_ohlcv_bullish):
        strategy = _make_strategy()
        signal = strategy.evaluate("AAPL", sample_ohlcv_bullish)
        assert signal.action == "buy"
        assert signal.strength > 0.0
        assert "Momentum detected" in signal.reason

    def test_hold_on_flat_data(self, sample_ohlcv_flat):
        strategy = _make_strategy()
        signal = strategy.evaluate("AAPL", sample_ohlcv_flat)
        assert signal.action == "hold"
        assert signal.strength == 0.0

    def test_hold_on_empty_data(self, sample_ohlcv_empty):
        strategy = _make_strategy()
        signal = strategy.evaluate("AAPL", sample_ohlcv_empty)
        assert signal.action == "hold"
        assert "Not enough data" in signal.reason

    def test_hold_on_single_bar(self, sample_ohlcv_single_bar):
        strategy = _make_strategy()
        signal = strategy.evaluate("AAPL", sample_ohlcv_single_bar)
        assert signal.action == "hold"
        assert "Not enough data" in signal.reason

    def test_missing_columns(self):
        strategy = _make_strategy()
        df = pd.DataFrame({"close": [100, 101], "volume": [1000, 2000]})
        signal = strategy.evaluate("AAPL", df)
        assert signal.action == "hold"
        assert "Missing required columns" in signal.reason

    def test_zero_open_price(self):
        strategy = _make_strategy()
        df = pd.DataFrame({
            "open": [0.0, 100.0],
            "close": [100.0, 105.0],
            "volume": [1000, 5000],
        })
        signal = strategy.evaluate("AAPL", df)
        assert signal.action == "hold"
        assert "zero" in signal.reason.lower()

    def test_configurable_thresholds(self, sample_ohlcv_bullish):
        # Very strict thresholds — should not trigger
        strategy = _make_strategy(price_threshold=50.0, volume_multiplier=100.0)
        signal = strategy.evaluate("AAPL", sample_ohlcv_bullish)
        assert signal.action == "hold"

    def test_strategy_name(self):
        strategy = _make_strategy()
        assert strategy.name == "momentum"

    def test_signal_ticker_preserved(self, sample_ohlcv_flat):
        strategy = _make_strategy()
        signal = strategy.evaluate("TSLA", sample_ohlcv_flat)
        assert signal.ticker == "TSLA"
