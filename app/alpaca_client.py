import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST, TimeFrame

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
API_KEY = os.getenv("APCA_API_KEY_ID")
API_SECRET = os.getenv("APCA_API_SECRET_KEY")
BASE_URL = os.getenv("APCA_API_BASE_URL")

# Initialize the Alpaca API client.
# REST is a class provided by the alpaca-trade-api package.
# When we create an instance of REST, we are creating an object
# that knows how to talk to Alpaca's API.
#
# This object (`api`) has built-in methods like:
# - get_account()
# - get_bars()
# - submit_order()
# - get_position()
# - list_orders()
# etc.
#
# It handles authentication using the API key/secret we provide.
api = REST(API_KEY, API_SECRET, BASE_URL)

def get_account():
    """Return the current account status."""
    return api.get_account()  # Returns an Account object with info like buying_power, equity, etc.

def get_bars(ticker: str, limit: int = 5, tf=TimeFrame.Minute):
    """
    Fetch recent bar (candlestick) data for a given symbol.

    Args:
        ticker (str): The stock symbol to fetch.
        limit (int): Number of bars to retrieve.
        tf (TimeFrame): Time frame (e.g. Minute, Day).

    Returns:
        pd.DataFrame: A dataframe containing OHLCV (open-high-low-close-volume) data.
    """
    bars = api.get_bars(ticker, timeframe=tf, limit=limit).df  # Returns a pandas DataFrame
    return bars

def submit_order(ticker: str, qty: int, side: str, type: str = 'market', time_in_force: str = 'gtc'):
    """
    Submit a trade order.

    Args:
        ticker (str): The stock symbol to trade.
        qty (int): Quantity of shares to buy/sell.
        side (str): 'buy' or 'sell'.
        type (str): Order type (default is 'market').
        time_in_force (str): How long the order remains active (default is 'gtc').
    """
    api.submit_order(
        symbol=ticker,               # Stock symbol to trade
        qty=qty,                     # Number of shares
        side=side,                   # 'buy' or 'sell'
        type=type,                   # Order type (e.g., 'market')
        time_in_force=time_in_force  # Duration the order stays open
    )
