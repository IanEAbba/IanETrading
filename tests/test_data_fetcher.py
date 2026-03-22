"""Tests for the DataFetcher module."""

from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest
from alpaca.common.exceptions import APIError

from src.data_fetcher import OHLCV_COLUMNS, DataFetcher, parse_timeframe


class TestParseTimeframe:

    def test_standard_timeframes(self):
        # TimeFrame objects don't support == by value, compare string representation
        assert str(parse_timeframe("1Min")) == "1Min"
        assert str(parse_timeframe("1Hour")) == "1Hour"
        assert str(parse_timeframe("1Day")) == "1Day"
        assert str(parse_timeframe("1Week")) == "1Week"
        assert str(parse_timeframe("1Month")) == "1Month"

    def test_custom_minute_timeframes(self):
        tf_5 = parse_timeframe("5Min")
        tf_15 = parse_timeframe("15Min")
        assert str(tf_5) == "5Min"
        assert str(tf_15) == "15Min"

    def test_invalid_timeframe_raises(self):
        with pytest.raises(ValueError, match="Unknown timeframe"):
            parse_timeframe("3Min")

        with pytest.raises(ValueError, match="Unknown timeframe"):
            parse_timeframe("invalid")


class TestDataFetcherFetch:

    def test_fetch_returns_dataframe_with_correct_columns(
        self, data_fetcher_config, mock_alpaca_client
    ):
        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)
        df = fetcher.fetch("AAPL")

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == OHLCV_COLUMNS
        assert len(df) == 5
        # Verify MultiIndex was flattened
        assert not isinstance(df.index, pd.MultiIndex)

    def test_fetch_returns_empty_on_no_data(
        self, data_fetcher_config, mock_empty_bars_response
    ):
        client = MagicMock()
        client.get_stock_bars.return_value = mock_empty_bars_response

        fetcher = DataFetcher(data_fetcher_config, client=client)
        df = fetcher.fetch("AAPL")

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == OHLCV_COLUMNS
        assert len(df) == 0

    def test_fetch_retries_on_api_error(self, data_fetcher_config, mock_bars_response):
        """API fails once then succeeds — tenacity retries."""
        client = MagicMock()
        client.get_stock_bars.side_effect = [
            APIError("rate limit"),
            mock_bars_response,
        ]

        fetcher = DataFetcher(data_fetcher_config, client=client)
        df = fetcher.fetch("AAPL")

        assert len(df) == 5
        assert client.get_stock_bars.call_count == 2

    def test_fetch_returns_empty_after_max_retries(self, data_fetcher_config):
        """All retries exhausted — returns empty DataFrame, doesn't crash."""
        client = MagicMock()
        client.get_stock_bars.side_effect = APIError("server error")

        fetcher = DataFetcher(data_fetcher_config, client=client)
        df = fetcher.fetch("AAPL")

        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == OHLCV_COLUMNS
        assert len(df) == 0
        # retry_attempts=2, so 2 calls total
        assert client.get_stock_bars.call_count == 2

    def test_fetch_uses_config_defaults(self, data_fetcher_config, mock_alpaca_client):
        """When no timeframe/limit args, uses config values."""
        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)
        fetcher.fetch("AAPL")

        call_args = mock_alpaca_client.get_stock_bars.call_args
        request = call_args[0][0]
        assert request.limit == 30
        # Timeframe should be 1Min (from config)
        assert str(request.timeframe) == "1Min"

    def test_fetch_override_timeframe_and_limit(
        self, data_fetcher_config, mock_alpaca_client
    ):
        """Explicit timeframe/limit args override config defaults."""
        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)
        fetcher.fetch("AAPL", timeframe="1Day", limit=10)

        call_args = mock_alpaca_client.get_stock_bars.call_args
        request = call_args[0][0]
        assert request.limit == 10
        assert str(request.timeframe) == "1Day"


class TestDataFetcherMultiple:

    def test_fetch_multiple_returns_dict(self, data_fetcher_config, mock_alpaca_client):
        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)
        results = fetcher.fetch_multiple(["AAPL", "MSFT"])

        assert isinstance(results, dict)
        assert set(results.keys()) == {"AAPL", "MSFT"}
        for ticker, df in results.items():
            assert isinstance(df, pd.DataFrame)
            assert list(df.columns) == OHLCV_COLUMNS


class TestDataFetcherCache:

    def test_cache_save_and_load(self, data_fetcher_config, mock_alpaca_client, tmp_path):
        """With cache enabled, data is saved and reloaded from CSV."""
        data_fetcher_config["data"]["cache_enabled"] = True
        data_fetcher_config["_root_dir"] = str(tmp_path)

        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)

        # First fetch — hits API, saves cache
        df1 = fetcher.fetch("AAPL")
        assert len(df1) == 5
        assert mock_alpaca_client.get_stock_bars.call_count == 1

        # Verify cache file exists
        cache_files = list((tmp_path / "data").glob("AAPL_*.csv"))
        assert len(cache_files) == 1

        # Second fetch — should load from cache, not API
        df2 = fetcher.fetch("AAPL")
        assert len(df2) == 5
        assert mock_alpaca_client.get_stock_bars.call_count == 1  # Still 1, no new API call

    def test_cache_skipped_when_disabled(
        self, data_fetcher_config, mock_alpaca_client, tmp_path
    ):
        """With cache disabled, no files are written."""
        data_fetcher_config["data"]["cache_enabled"] = False
        data_fetcher_config["_root_dir"] = str(tmp_path)

        fetcher = DataFetcher(data_fetcher_config, client=mock_alpaca_client)
        fetcher.fetch("AAPL")

        # No data/ directory or files should exist
        data_dir = tmp_path / "data"
        if data_dir.exists():
            assert len(list(data_dir.glob("*.csv"))) == 0
