"""Shared test fixtures for IanETrading."""

from unittest.mock import MagicMock

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


@pytest.fixture
def mock_bars_response(sample_ohlcv_bullish):
    """Mock alpaca-py BarSet response with .df returning a MultiIndex DataFrame.

    Simulates what StockHistoricalDataClient.get_stock_bars() returns.
    The real response has a MultiIndex (symbol, timestamp).
    """
    # Build MultiIndex DataFrame like Alpaca returns
    df = sample_ohlcv_bullish.copy()
    df["trade_count"] = [50, 55, 45, 52, 200]
    df["vwap"] = [100.5, 101.5, 102.5, 103.5, 105.5]

    # Create MultiIndex with symbol level
    symbol_index = pd.MultiIndex.from_arrays(
        [["AAPL"] * len(df), range(len(df))],
        names=["symbol", "timestamp"],
    )
    df.index = symbol_index

    # Create mock BarSet with .df property
    mock_barset = MagicMock()
    mock_barset.df = df
    return mock_barset


@pytest.fixture
def mock_empty_bars_response():
    """Mock BarSet with empty DataFrame."""
    mock_barset = MagicMock()
    mock_barset.df = pd.DataFrame()
    return mock_barset


@pytest.fixture
def mock_alpaca_client(mock_bars_response):
    """Mock StockHistoricalDataClient that returns bars."""
    client = MagicMock()
    client.get_stock_bars.return_value = mock_bars_response
    return client


@pytest.fixture
def sample_buy_signal():
    """Single buy Signal for testing."""
    from src.strategies.base import Signal

    return Signal(ticker="AAPL", action="buy", strength=0.85, reason="Volume spike + breakout")


@pytest.fixture
def sample_signals():
    """Mixed list of Signals: buy, sell, and hold."""
    from src.strategies.base import Signal

    return [
        Signal(ticker="AAPL", action="buy", strength=0.85, reason="Volume spike"),
        Signal(ticker="MSFT", action="sell", strength=0.60, reason="Breakdown detected"),
        Signal(ticker="NVDA", action="hold", strength=0.0, reason="No signal"),
    ]


@pytest.fixture
def trade_executor_config(tmp_path):
    """Config dict for TradeExecutor tests with temp log directory."""
    return {
        "alpaca": {
            "key_id": "test_key",
            "secret_key": "test_secret",
            "base_url": "https://paper-api.alpaca.markets",
        },
        "execution": {
            "mode": "dry-run",
            "default_qty": 1,
            "log_trades": False,
        },
        "_root_dir": str(tmp_path),
    }


@pytest.fixture
def data_fetcher_config(tmp_path):
    """Config dict for DataFetcher tests with temp cache directory."""
    return {
        "alpaca": {
            "key_id": "test_key",
            "secret_key": "test_secret",
        },
        "data": {
            "timeframe": "1Min",
            "bar_limit": 30,
            "cache_enabled": False,
            "retry_attempts": 2,  # Low for faster tests
        },
        "_root_dir": str(tmp_path),
    }
