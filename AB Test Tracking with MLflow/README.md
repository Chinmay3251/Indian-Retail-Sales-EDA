# W9D3 — A/B Test Tracking with MLflow

## Objective
Analyze a control and treatment experiment, calculate conversion metrics and a two-sided two-proportion z-test, and track the comparison in MLflow.

## Project files
- `src/ab_test_tracking.py` — validates input, calculates variant metrics and significance, and logs the experiment.
- `data/sample_ab_test.csv` — small sample dataset for practice.
- `tests/test_ab_test_tracking.py` — tests the analysis and validation.
- `requirements.txt` — dependencies.

## Required CSV columns
`user_id`, `variant`, `converted`, `revenue`. The `variant` field must contain `control` and `treatment`; `converted` must be 0 or 1.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the experiment
```powershell
python src/ab_test_tracking.py
```
Use another CSV or experiment:
```powershell
python src/ab_test_tracking.py --csv data/sample_ab_test.csv --experiment W9D3-Checkout-AB-Test
```

## View MLflow runs
Open a second PowerShell terminal:
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Visit `http://127.0.0.1:5000`. The parent run records comparison-level results; nested child runs record control and treatment metrics separately.

## Logged parameters, metrics and artifacts
- Parameters: dataset, test type, variants, significance threshold.
- Variant metrics: users, conversions, conversion rate, average revenue, total revenue.
- Comparison metrics: absolute conversion difference, relative uplift, z-score, p-value, significance flag.
- Artifact: JSON report of the calculated results.

## Interpretation and limitations
A p-value below 0.05 is treated as statistically significant for this practice exercise. This is a two-sided two-proportion z-test for conversion rates. It assumes independent observations and a suitable large-sample approximation. It does not test revenue differences or correct for multiple comparisons. Statistical significance does not establish business importance or causation if experiment assignment/data quality is flawed. The sample CSV is illustrative; use the assigned dataset for actual analysis.

## Tests
```powershell
pytest -q
```

## Git tasks
```powershell
git checkout -b feat/w9d3-[name]
git add .
git commit -m "feat: add A/B test analysis and MLflow tracking"
git add README.md tests/
git commit -m "test: add A/B test validation and usage documentation"
git push -u origin feat/w9d3-[name]
```
Replace `[name]` with your assigned suffix. Verify with `git log -2 --oneline` and update your PR.
