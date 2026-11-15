import pandas as pd

def prepare_market_data(frame):
    if frame.empty: raise ValueError("Market data is empty.")
    date_col = next((c for c in ["Date","Datetime","ds"] if c in frame.columns), None)
    value_col = next((c for c in ["Adj Close","Close","y"] if c in frame.columns), None)
    if not date_col or not value_col:
        raise ValueError("CSV must contain Date/Datetime and Adj Close/Close columns.")
    out = pd.DataFrame({"ds":pd.to_datetime(frame[date_col],errors="coerce"),
                        "y":pd.to_numeric(frame[value_col],errors="coerce")})
    if out["ds"].dt.tz is not None: out["ds"] = out["ds"].dt.tz_localize(None)
    out = out.dropna().drop_duplicates("ds").sort_values("ds").reset_index(drop=True)
    if len(out)<30: raise ValueError("At least 30 valid observations are required.")
    if (out.y<=0).any(): raise ValueError("Prices must be positive.")
    return out

def load_csv(path):
    return prepare_market_data(pd.read_csv(path))

def download_market_data(ticker, years=5):
    import yfinance as yf
    raw=yf.download(ticker,period=f"{years}y",interval="1d",auto_adjust=False,progress=False)
    if raw.empty: raise RuntimeError(f"No data returned for {ticker}. Check ticker or connection.")
    if isinstance(raw.columns,pd.MultiIndex): raw.columns=raw.columns.get_level_values(0)
    return prepare_market_data(raw.reset_index())
