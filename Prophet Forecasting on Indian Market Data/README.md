# W10D2 — Prophet Forecasting on Indian Market Data

Forecast Indian market prices with Prophet. Default ticker: `^NSEI` (NIFTY 50); examples include `RELIANCE.NS`, `TCS.NS`, and `INFY.NS`.

**Warning:** This is an educational forecasting exercise, not investment advice. Forecasts are uncertain and should not be used alone for trading decisions.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run
Download 5 years of NIFTY 50 history and forecast 90 calendar days:
```powershell
python -m src.forecast --ticker "^NSEI" --years 5 --period 90
```
For a stock:
```powershell
python -m src.forecast --ticker "RELIANCE.NS" --years 5 --period 180
```
Offline demonstration using included **synthetic (not real market)** data:
```powershell
python -m src.forecast --input data/sample_indian_market.csv --period 90
```

## Outputs
`outputs/forecast.csv`, `outputs/forecast.png`, `outputs/model_summary.json`, and `outputs/metrics.json` (when holdout metrics are available).

## Method
1. Fetch daily Yahoo Finance OHLC data with yfinance, or load a CSV.
2. Use adjusted close where available, otherwise close.
3. Clean dates/prices and convert to Prophet's `ds` / `y` schema.
4. Evaluate chronologically using the latest 20% as holdout; report MAE and RMSE.
5. Fit on all observations and forecast future calendar days.
6. Save forecast values, uncertainty intervals, metrics, and chart.

Prophet's daily calendar forecast includes weekends and exchange holidays, when NSE has no trading. Interpret those dates cautiously.

## Optional dashboard
```powershell
streamlit run app.py
```
Choose online ticker data or bundled synthetic sample, then click Run forecast.

## Git workflow
```powershell
git checkout -b feat/w10d2-prophet-indian-market
git add .
git commit -m "feat: add Prophet forecasting for Indian market data"
git add README.md tests
git commit -m "test: add data validation checks and document workflow"
git push -u origin feat/w10d2-prophet-indian-market
git log -2 --oneline
git status
```
If branch already exists, use `git checkout feat/w10d2-prophet-indian-market`. Check `git remote -v` to confirm `origin` exists before pushing.
