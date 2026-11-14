# W9D1 — MLflow Tracking: Log Data Analytics Experiments

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Run an experiment
```powershell
python src/track_experiment.py
```
Optional:
```powershell
python src/track_experiment.py --csv data/sample_sales.csv --experiment W9D1-Sales --run-name baseline
```

## View runs
Open another PowerShell terminal:
```powershell
mlflow ui --backend-store-uri ./mlruns --port 5000
```
Visit http://127.0.0.1:5000. Run the script again with another run name to compare runs.

## Logged information
- Parameters: dataset name, analysis type, row count, column count.
- Metrics: numeric/categorical column counts, missing cells/rate, duplicate rows.
- Artifacts: JSON profile and numeric descriptive-statistics CSV.

## Limitations
This is a CSV data-profiling experiment, not model training. Metrics describe the input data and do not prove business causation. Replace the sample CSV with your assigned dataset if needed.

## Git
```powershell
git checkout -b feat/w9d1-[name]
git add .
git commit -m "feat: add MLflow data analytics experiment tracking"
git add README.md src/track_experiment.py
git commit -m "docs: document MLflow setup and experiment outputs"
git push -u origin feat/w9d1-[name]
```
