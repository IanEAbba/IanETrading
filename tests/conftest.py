"""Shared test fixtures for IanETrading."""

import pandas as pd
import pytest


@pytest.fixture
def sample_ohlcv_bullish():
    """OHLCV DataFrame showing bullish momentum (price up, volume spike)."""
    return pd.DataFrame({
        "open": [100.0, 101.0, 102.0, 103.0, 104.0],
        "high": [101.5, 102.5, 103.5, 104.5, 108.0],
        "low": [99.5, 100.5, 101.5, 102.5, 103.5],
        "close": [101.0, 102.0, 103.0, 104.0, 107.0],
        "volume": [1000, 1100, 900, 1050, 5000],  # Last bar: ~4.7x avg
    })


@pytest.fixture
def sample_ohlcv_flat():
    """OHLCV DataFrame with no significant movement."""
    return pd.DataFrame({
        "open": [100.0, 100.1, 100.0, 99.9, 100.0],
        "high": [100.5, 100.5, 100.4, 100.3, 100.2],
        "low": [99.5, 99.6, 99.6, 99.5, 99.8],
        "close": [100.1, 100.0, 99.9, 100.0, 100.1],
        "volume": [1000, 1050, 980, 1020, 1010],
    })


@pytest.fixture
def sample_ohlcv_empty():
    """Empty OHLCV DataFrame."""
    return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])


@pytest.fixture
def sample_ohlcv_single_bar():
    """OHLCV DataFrame with only one bar (insufficient for evaluation)."""
    return pd.DataFrame({
        "open": [100.0],
        "high": [101.0],
        "low": [99.0],
        "close": [100.5],
        "volume": [1000],
    })


@pytest.fixture
def sample_config():
    """Minimal config dict for testing."""
    return {
        "alpaca": {
            "key_id": "test_key",
            "secret_key": "test_secret",
            "base_url": "https://paper-api.alpaca.markets",
        },
        "tickers": ["AAPL", "MSFT"],
        "data": {
            "timeframe": "1Min",
            "bar_limit": 30,
            "cache_enabled": False,
            "retry_attempts": 3,
        },
        "strategies": {
            "momentum": {
                "enabled": True,
                "price_threshold": 1.0,
                "volume_multiplier": 2.0,
            }
        },
        "execution": {
            "mode": "dry-run",
            "default_qty": 1,
            "log_trades": True,
        },
    }
