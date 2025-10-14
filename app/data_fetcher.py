import os
import time
import pandas as pd
import requests
from datetime import datetime
from typing import List, Optional
from requests.exceptions import RequestException


class DataFetcher:
    """
    Fetches OHLCV data for Smart Money strategy from Alpaca or other APIs.
    Handles retries, caching, and export to CSV.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        base_url: str = "https://data.alpaca.markets/v2",
        cache_dir: str = os.path.join(os.path.dirname(__file__), "..", "data"),
        max_retries: int = 3,
        retry_delay: int = 3,
    ):
        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.api_secret = api_secret or os.getenv("ALPACA_SECRET_KEY")
        self.base_url = base_url
        self.cache_dir = os.path.abspath(cache_dir)
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        os.makedirs(self.cache_dir, exist_ok=True)

        self.headers = {
            "APCA-API-KEY-ID": self.api_key,
            "APCA-API-SECRET-KEY": self.api_secret,
        }

    def fetch(self, symbols: List[str], timeframe: str = "1Day", limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data for given symbols and timeframe."""
        all_data = []

        for symbol in symbols:
            for attempt in range(1, self.max_retries + 1):
                try:
                    url = f"{self.base_url}/stocks/{symbol}/bars"
                    params = {"timeframe": timeframe, "limit": limit}
                    response = requests.get(url, headers=self.headers, params=params, timeout=10)
                    response.raise_for_status()

                    data = response.json().get("bars", [])
                    if not data:
                        print(f"⚠️ No data for {symbol}")
                        continue

                    df = pd.DataFrame(data)
                    df["symbol"] = symbol
                    all_data.append(df)
                    print(f"✅ Fetched {len(df)} bars for {symbol}")
                    break

                except RequestException as e:
                    print(f"⚠️ Attempt {attempt}/{self.max_retries} failed for {symbol}: {e}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)
                    else:
                        print(f"❌ Giving up on {symbol}")

        if not all_data:
            return pd.DataFrame()

        combined = pd.concat(all_data)
        combined["t"] = pd.to_datetime(combined["t"])
        combined = combined.rename(
            columns={
                "t": "timestamp",
                "o": "open",
                "h": "high",
                "l": "low",
                "c": "close",
                "v": "volume",
            }
        )
        return combined[["timestamp", "symbol", "open", "high", "low", "close", "volume"]]

    def export_csv(self, df: pd.DataFrame) -> str:
        """Export DataFrame to timestamped CSV in cache_dir."""
        if df.empty:
            print("⚠️ No data to export.")
            return ""

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.cache_dir, f"latest_{timestamp}.csv")
        df.to_csv(file_path, index=False)
        print(f"💾 Data exported to {file_path}")
        return file_path


if __name__ == "__main__":
    fetcher = DataFetcher()
    df = fetcher.fetch(["AAPL", "NVDA", "TSLA"], timeframe="1Day", limit=10)
    fetcher.export_csv(df)
