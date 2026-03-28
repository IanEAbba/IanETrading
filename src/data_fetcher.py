"""DataFetcher — Alpaca Markets data retrieval with retry and caching.

Wraps the alpaca-py StockHistoricalDataClient to fetch OHLCV bar data
with automatic retry on transient failures and optional CSV caching.
"""

import logging
from datetime import date
from pathlib import Path

import pandas as pd
from alpaca.common.exceptions import APIError
from alpaca.data.enums import Adjustment, DataFeed
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Standard OHLCV columns that downstream modules expect
OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]

# Mapping from config strings to TimeFrame objects
_TIMEFRAME_MAP = {
    "1Min": TimeFrame.Minute,
    "5Min": TimeFrame(5, TimeFrameUnit.Minute),
    "15Min": TimeFrame(15, TimeFrameUnit.Minute),
    "30Min": TimeFrame(30, TimeFrameUnit.Minute),
    "1Hour": TimeFrame.Hour,
    "1Day": TimeFrame.Day,
    "1Week": TimeFrame.Week,
    "1Month": TimeFrame.Month,
}


def parse_timeframe(tf_string: str) -> TimeFrame:
    """Convert a config timeframe string to an alpaca-py TimeFrame object.

    Args:
        tf_string: Timeframe string (e.g. "1Min", "5Min", "1Hour", "1Day").

    Returns:
        Corresponding TimeFrame object.

    Raises:
        ValueError: If the string doesn't match any known timeframe.
    """
    if tf_string in _TIMEFRAME_MAP:
        return _TIMEFRAME_MAP[tf_string]
    raise ValueError(
        f"Unknown timeframe '{tf_string}'. "
        f"Valid options: {', '.join(_TIMEFRAME_MAP.keys())}"
    )


class DataFetcher:
    """Fetches OHLCV market data from Alpaca Markets API.

    Uses alpaca-py StockHistoricalDataClient with tenacity retry logic
    and optional CSV caching to the data/ directory.

    Args:
        config: Full config dict from load_config().
        client: Optional pre-built StockHistoricalDataClient (for testing).
    """

    def __init__(self, config: dict, client: StockHistoricalDataClient | None = None):
        alpaca_cfg = config.get("alpaca", {})
        data_cfg = config.get("data", {})

        # Build client if not injected (dependency injection for testing)
        if client is not None:
            self._client = client
        else:
            self._client = StockHistoricalDataClient(
                api_key=alpaca_cfg.get("key_id"),
                secret_key=alpaca_cfg.get("secret_key"),
            )

        # Data settings with defaults
        self._default_timeframe = data_cfg.get("timeframe", "1Min")
        self._default_limit = data_cfg.get("bar_limit", 30)
        self._cache_enabled = data_cfg.get("cache_enabled", False)
        self._retry_attempts = data_cfg.get("retry_attempts", 3)

        # Cache directory
        self._cache_dir = Path(config.get("_root_dir", ".")) / "data"
        if self._cache_enabled:
            self._cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch(
        self,
        ticker: str,
        timeframe: str | None = None,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """Fetch OHLCV bars for a single ticker.

        Args:
            ticker: Stock symbol (e.g. "AAPL").
            timeframe: Override config timeframe (e.g. "1Min", "5Min", "1Day").
            limit: Override config bar_limit.

        Returns:
            DataFrame with columns [open, high, low, close, volume].
            Returns empty DataFrame with correct columns on failure.
        """
        tf_str = timeframe or self._default_timeframe
        bar_limit = limit or self._default_limit

        # Check cache first
        if self._cache_enabled:
            cached = self._load_cache(ticker)
            if cached is not None:
                logger.info("[%s] Loaded %d bars from cache", ticker, len(cached))
                return cached

        # Fetch from API with retry
        try:
            df = self._fetch_with_retry(ticker, tf_str, bar_limit)
        except (APIError, ConnectionError) as e:
            logger.error("[%s] Failed to fetch after retries: %s", ticker, e)
            return pd.DataFrame(columns=OHLCV_COLUMNS)

        if df.empty:
            logger.warning("[%s] API returned no bars", ticker)
            return pd.DataFrame(columns=OHLCV_COLUMNS)

        # Standardize columns — keep only OHLCV
        df = self._standardize(df)

        # Cache if enabled
        if self._cache_enabled:
            self._save_cache(ticker, df)

        logger.info("[%s] Fetched %d bars", ticker, len(df))
        return df

    def fetch_multiple(self, tickers: list[str]) -> dict[str, pd.DataFrame]:
        """Fetch bars for multiple tickers.

        Args:
            tickers: List of stock symbols.

        Returns:
            Dict mapping ticker → OHLCV DataFrame.
        """
        results = {}
        for ticker in tickers:
            results[ticker] = self.fetch(ticker)
        return results

    def _fetch_with_retry(self, ticker: str, tf_str: str, limit: int) -> pd.DataFrame:
        """Fetch bars with tenacity retry on transient failures.

        Retries on APIError (429, 5xx) and ConnectionError.
        Uses exponential backoff: 1s, 2s, 4s...

        Args:
            ticker: Stock symbol.
            tf_str: Timeframe string.
            limit: Number of bars.

        Returns:
            Raw DataFrame from Alpaca API.

        Raises:
            APIError: If all retries exhausted.
            ConnectionError: If network unreachable after retries.
        """
        tf = parse_timeframe(tf_str)

        @retry(
            stop=stop_after_attempt(self._retry_attempts),
            wait=wait_exponential(multiplier=1, min=1, max=16),
            retry=retry_if_exception_type((APIError, ConnectionError, OSError)),
            reraise=True,
        )
        def _do_fetch() -> pd.DataFrame:
            request = StockBarsRequest(
                symbol_or_symbols=ticker,
                timeframe=tf,
                limit=limit,
                feed=DataFeed.IEX,
                adjustment=Adjustment.RAW,
            )
            bars = self._client.get_stock_bars(request)
            return bars.df

        return _do_fetch()

    def _standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize Alpaca DataFrame to OHLCV columns with flat index.

        Args:
            df: Raw DataFrame from Alpaca (may have MultiIndex with symbol).

        Returns:
            DataFrame with columns [open, high, low, close, volume] and
            a simple DatetimeIndex (or RangeIndex if reset).
        """
        # Alpaca returns MultiIndex (symbol, timestamp) for single-symbol requests
        if isinstance(df.index, pd.MultiIndex):
            df = df.droplevel("symbol")

        # Keep only OHLCV columns (drop trade_count, vwap if present)
        available = [col for col in OHLCV_COLUMNS if col in df.columns]
        df = df[available].copy()

        # Reset index to make timestamp a column (simpler for downstream)
        df = df.reset_index(drop=True)

        return df

    def _cache_path(self, ticker: str) -> Path:
        """Return cache file path for a ticker.

        Format: data/{TICKER}_{YYYY-MM-DD}.csv
        """
        today = date.today().isoformat()
        return self._cache_dir / f"{ticker}_{today}.csv"

    def _save_cache(self, ticker: str, df: pd.DataFrame) -> None:
        """Save DataFrame to CSV cache."""
        path = self._cache_path(ticker)
        df.to_csv(path, index=False)
        logger.debug("[%s] Cached %d bars to %s", ticker, len(df), path)

    def _load_cache(self, ticker: str) -> pd.DataFrame | None:
        """Load DataFrame from cache if exists and is from today.

        Returns:
            DataFrame if cache hit, None if miss.
        """
        path = self._cache_path(ticker)
        if not path.exists():
            return None

        try:
            df = pd.read_csv(path)
            if df.empty or not set(OHLCV_COLUMNS).issubset(df.columns):
                return None
            return df
        except Exception:
            logger.warning("[%s] Failed to read cache at %s", ticker, path)
            return None
