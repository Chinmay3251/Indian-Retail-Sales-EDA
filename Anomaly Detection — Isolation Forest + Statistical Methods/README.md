# W10D3 — Anomaly Detection: Isolation Forest + Statistical Methods

A practical anomaly-detection project for tabular business data. It combines:
- **Z-score**: flags observations unusually far from the mean.
- **IQR**: flags observations outside the 1.5 × IQR fences.
- **Isolation Forest**: unsupervised machine-learning model that isolates unusual observations.

The included dataset is synthetic retail transaction data. It is for learning and testing, not real customer or market records.

## 1. Setup (Windows PowerShell)

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

## 2. Run the analysis

```powershell
python -m src.detect --input data/sample_transactions.csv --output outputs --contamination 0.04
```

Optional columns can be selected. By default, the script analyzes numeric columns except `transaction_id`.

```powershell
python -m src.detect --input data/sample_transactions.csv --output outputs --features amount,items --contamination 0.04
```

## 3. Outputs

The `outputs/` folder contains:
- `anomaly_results.csv` — original records plus Z-score, IQR, Isolation Forest, and combined flags.
- `summary.json` — row counts, feature names, thresholds, and method totals.
- `anomaly_plot.png` — feature distribution with Isolation Forest anomalies highlighted.

A record is marked `any_anomaly` if at least one selected method flags it. Review individual method flags before taking action.

## 4. Methodology

1. Load and validate the CSV.
2. Select numeric features and impute missing feature values with the column median.
3. Calculate absolute Z-scores; flag values above 3 by default.
4. Calculate IQR fences; flag values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR.
5. Fit Isolation Forest using the selected numeric features and a configurable contamination rate.
6. Combine method flags and save results and a chart.

### Important interpretation notes

- Z-score works best when a feature's distribution is reasonably well-behaved; extreme skew can affect its usefulness.
- IQR is more robust to extreme values, but still flags univariate extremes feature by feature.
- Isolation Forest considers patterns across selected features.
- An anomaly is not automatically an error, fraud, or a business problem. Investigate context before acting.
- Scale and feature selection can influence results. This starter project uses median imputation and Isolation Forest's tree-based model without mandatory standardization.

## 5. Run tests

```powershell
pytest -q
```

## 6. Git workflow

```powershell
git checkout -b feat/w10d3-anomaly-detection
git add .
git commit -m "feat: implement statistical and isolation forest anomaly detection"
git add README.md tests
git commit -m "test: add anomaly detection checks and document workflow"
git push -u origin feat/w10d3-anomaly-detection
git log -2 --oneline
git status
```

If the branch already exists, use `git checkout feat/w10d3-anomaly-detection`. Check `git remote -v` before pushing if you are unsure whether `origin` is configured.
