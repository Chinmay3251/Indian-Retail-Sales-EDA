# W10D1 — Time Series Analysis: Trends, Seasonality, ARIMA

## What it does
Loads regularly spaced time-series data, plots observed values, decomposes trend/seasonality when enough data is available, runs an Augmented Dickey-Fuller test, fits an ARIMA(p,d,q) baseline, evaluates a holdout forecast, and logs parameters, metrics and plots to MLflow.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Run
```powershell
python src/analysis.py
```
Custom data:
```powershell
python src/analysis.py --csv data/your_data.csv --date-col date --value-col sales --freq MS --order 1,1,1 --period 12 --test-size 6
```
Frequency examples: `D` daily, `W` weekly, `MS` month-start.

## Outputs and MLflow
Creates observed, decomposition and forecast plots plus a JSON report under `artifacts/`. Logs parameters, MAE, RMSE, ADF statistic/p-value and artifacts to the `W10D1-Time-Series-ARIMA` experiment.
View runs:
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Open http://127.0.0.1:5000.

## Tests
```powershell
pytest -q
```

## Limitations
The sample data is synthetic. ARIMA(1,1,1) is a baseline, not an optimized model. The seasonal period is used for classical decomposition; this is not SARIMA. Interpret ADF results with plots and domain knowledge.

## Git tasks
```powershell
git checkout -b feat/w10d1-[name]
git add .
git commit -m "feat: add time series decomposition and ARIMA forecasting"
git add README.md tests/
git commit -m "test: add time series tests and documentation"
git push -u origin feat/w10d1-[name]
```
Replace `[name]` with your suffix. Verify using `git log -2 --oneline` and update your PR.
