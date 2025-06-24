import pandas as pd
import yfinance as yf

def fetch_data(ticker, start, end, interval="1d"):
    df = yf.download(
        tickers=ticker,
        start=start, end=end,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )
    # If there's a MultiIndex on columns, drop the ticker level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(level=1)  # keep price-level names only

    df.index = df.index.tz_localize(None)
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]
