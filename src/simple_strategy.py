# simple_strategy.py
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from ingestion import fetch_data

def flatten_multiindex(df):
    # df is now a multi-index DataFrame (column tuples)
    close = df['Close']  # just the close-price columns for each ticker
    close.columns.name = None  # clean up column name
    return close


def add_indicators(df):
    df['RSI'] = ta.rsi(df['Close'], length=14)
    df['SMA20'] = df['Close'].rolling(20).mean()
    df['SMA50'] = df['Close'].rolling(50).mean()
    return df

def generate_signals(df):
    df = add_indicators(df)
    df['signal'] = 0
    cond = (
        (df['RSI'] < 30)
        & (df['SMA20'].shift() < df['SMA50'].shift())
        & (df['SMA20'] > df['SMA50'])
    )
    df.loc[cond, 'signal'] = 1
    return df

if __name__=="__main__":
    # Fetch multi-ticker with yfinance
    raw = fetch_data(["RELIANCE.NS", "TCS.NS"], "2025-01-01", "2025-06-20")
    close_df = flatten_multiindex(raw)
    for ticker in close_df.columns:
        df = close_df[[ticker]].rename(columns={ticker: 'Close'})
        df = generate_signals(df)
        print(f"\n--- {ticker} ---")
        print(df.tail())
