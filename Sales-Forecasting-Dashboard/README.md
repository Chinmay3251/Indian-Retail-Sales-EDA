# Week 10 Project — Sales Forecasting Dashboard

A complete interactive sales forecasting project using Python, Streamlit, Plotly, and Statsmodels. It combines historical sales exploration, forecasting, model comparison, evaluation, and downloadable outputs.

> The included dataset is synthetic training data. Forecasts are estimates for learning and planning, not guarantees.

## Features
- Load the bundled monthly sales data or upload your own CSV
- Interactive historical sales trend and monthly seasonality charts
- Forecast using Naive, Moving Average, and Holt-Winters Exponential Smoothing
- Compare models using chronological holdout MAE and RMSE
- Forecast horizon and moving-average window controls
- KPI cards, forecast table, and CSV download
- Save forecast chart and metrics to `outputs/`

## Dataset format
Uploaded CSVs must contain:
- `date`: date or timestamp
- `sales`: numeric sales value

The sample file contains 72 synthetic monthly observations with trend, seasonality, and random variation.

## Setup — Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Run the dashboard

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Run from the command line

```powershell
python -m src.pipeline --input data/monthly_sales.csv --horizon 6 --output outputs
```

## Methodology
1. Validate date and sales columns, parse dates, remove invalid rows and duplicate dates.
2. Visualize historical sales and month-of-year patterns.
3. Split observations chronologically: the latest 20% is the holdout test set.
4. Fit each method on training observations and calculate MAE and RMSE.
5. Select the method with the lowest holdout RMSE (dashboard selection can override this).
6. Refit the chosen method on all observations and forecast the requested number of periods.
7. Save forecast data, model comparison metrics, and a Plotly chart.

### Forecasting methods
- **Naive:** repeats the last observed sales value.
- **Moving Average:** repeats the mean of the latest configurable window.
- **Holt-Winters:** fits additive trend and additive seasonality when sufficient monthly history is available; otherwise the pipeline uses trend-only exponential smoothing.

### Metrics
- **MAE:** average absolute difference between actual and predicted values.
- **RMSE:** square root of the average squared prediction error; it penalizes larger errors more strongly.

A low holdout error does not guarantee future accuracy. Review data quality, business context, promotions, stock-outs, and market changes before using forecasts for decisions.

## Tests

```powershell
pytest -q
```

## Git workflow

```powershell
git checkout -b feat/w10d5-sales-forecasting-dashboard
git add .
git commit -m "feat: build end-to-end sales forecasting dashboard"
git add README.md tests
git commit -m "test: add forecasting pipeline tests and project documentation"
git push -u origin feat/w10d5-sales-forecasting-dashboard
git log -2 --oneline
git status
```

If the branch already exists, use `git checkout feat/w10d5-sales-forecasting-dashboard`. Check `git remote -v` to confirm `origin` is configured before pushing.
