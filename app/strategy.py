import pandas as pd

def check_momentum(df: pd.DataFrame, price_thresh=1.0, volume_multiplier=2.0) -> bool:
    """
    Determine if a symbol shows momentum worth buying.

    Args:
        df (pd.DataFrame): OHLCV data (must include 'open', 'close', 'volume').
        price_thresh (float): Minimum % increase in price to trigger signal.
        volume_multiplier (float): Volume must exceed avg volume by this factor.

    Returns:
        bool: True if momentum signal is detected, False otherwise.
    """
    if len(df) < 2:
        return False  # Not enough data to evaluate

    price_change = (df['close'].iloc[-1] - df['open'].iloc[0]) / df['open'].iloc[0] * 100
    avg_volume = df['volume'].mean()
    last_volume = df['volume'].iloc[-1]

    if price_change >= price_thresh and last_volume > avg_volume * volume_multiplier:
        print(f"Buy signal detected! Price change: {price_change:.2f}%, Volume spike: {last_volume} > {avg_volume:.0f}")
        return True
    else:
        print(f"No signal. Price change: {price_change:.2f}%, Volume: {last_volume}")
        return False
