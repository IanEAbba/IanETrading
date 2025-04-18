import os
from dotenv import load_dotenv
from alpaca_trade_api.rest import REST
import pandas as pd

load_dotenv()

# Alpaca API 연결
api = REST(
    os.getenv("APCA_API_KEY_ID"),
    os.getenv("APCA_API_SECRET_KEY"),
    os.getenv("APCA_API_BASE_URL")
)

# 종목 모멘텀 체크 함수
def check_momentum(ticker):
    try:
        bars = api.get_bars(ticker, timeframe="1Min", limit=30).df
        if len(bars) < 2:
            return

        latest_price = bars['close'].iloc[-1]
        past_price = bars['close'].iloc[0]
        volume = bars['volume'].iloc[-1]
        avg_volume = bars['volume'].mean()

        pct_change = (latest_price - past_price) / past_price * 100

        if pct_change > 1.0 and volume > avg_volume * 1.5:
            print(f"[{ticker}] 모멘텀 감지! +{pct_change:.2f}%, 거래량 증가!")
        else:
            print(f"[{ticker}] 조건 불충족: +{pct_change:.2f}%")

    except Exception as e:
        print(f"[{ticker}] 에러 발생: {e}")

# 테스트용 종목 리스트
tickers = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]

for ticker in tickers:
    check_momentum(ticker)
