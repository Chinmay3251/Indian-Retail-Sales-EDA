# W10D4 — Forecasting Dashboard with Plotly + Streamlit

An interactive time-series forecasting dashboard built with Streamlit and Plotly. It includes a synthetic monthly sales dataset and lets you explore historical trends, choose a forecasting method, adjust the forecast horizon, and inspect forecast values and error metrics.

> The bundled dataset is synthetic and intended for practice. Forecasts are estimates, not guarantees.

## Features
- Interactive historical sales line chart using Plotly
- Date range and forecast horizon controls
- Forecasting methods: Naive, Moving Average, and Exponential Smoothing
- Holdout evaluation using MAE and RMSE
- Forecast table and CSV download
- KPI cards for latest actual value, forecast average, and evaluation metrics

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

## Run the dashboard

From the project root:

```powershell
streamlit run app.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Forecast methods
- **Naive:** repeats the most recent observed value.
- **Moving Average:** repeats the average of the latest window of observations.
- **Exponential Smoothing:** fits a level/trend/seasonal model using Statsmodels when enough observations are available.

The dashboard evaluates each selected method on the latest 20% of observations using a chronological split. MAE and RMSE are calculated on that holdout. The forecast is then refitted using all filtered observations.

## Dataset
`data/monthly_sales.csv` contains 72 synthetic monthly observations with a trend and seasonal variation. Replace it with your own CSV containing:
- `date`: date or timestamp
- `sales`: numeric target value

Use the sidebar's upload control to load another CSV.

## Tests

```powershell
pytest -q
```

## Git workflow

```powershell
git checkout -b feat/w10d4-forecasting-dashboard
git add .
git commit -m "feat: build interactive forecasting dashboard with Plotly and Streamlit"
git add README.md tests
git commit -m "test: add forecasting method checks and document dashboard"
git push -u origin feat/w10d4-forecasting-dashboard
git log -2 --oneline
git status
```

If the branch already exists, use `git checkout feat/w10d4-forecasting-dashboard`. Check `git remote -v` before pushing if you are unsure whether `origin` is configured.
