# W9D5 — Tracked Data Analytics Experiment Pipeline

## Objective
Build an end-to-end classification analytics pipeline that profiles a CSV dataset, preprocesses numeric and categorical fields, trains a baseline Logistic Regression model, evaluates it, and tracks the run with MLflow.

## Pipeline stages
1. Load and validate the CSV and target column.
2. Separate features and target; remove rows with missing target values.
3. Split data into training and test sets.
4. Impute missing numeric/categorical values, scale numeric fields, and one-hot encode categorical fields.
5. Train a Logistic Regression classifier.
6. Calculate accuracy, weighted precision, weighted recall, weighted F1, and ROC-AUC for binary targets when available.
7. Log parameters, data-quality metrics, evaluation metrics, the trained model, and a JSON report to MLflow.

## Project structure
- `src/pipeline.py` — end-to-end pipeline and MLflow tracking.
- `data/sample_customer_churn.csv` — small practice dataset.
- `tests/test_pipeline.py` — checks data preparation and preprocessing/model pipeline.
- `requirements.txt` — dependencies.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
From the project root:
```powershell
python src/pipeline.py
```
Use another CSV:
```powershell
python src/pipeline.py --csv data/your_dataset.csv --target churn --experiment W9D5-Customer-Analytics --run-name baseline-v1
```

## View MLflow experiment
Open a second PowerShell terminal:
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Open `http://127.0.0.1:5000`, select `W9D5-Tracked-Analytics-Pipeline`, and inspect run parameters, metrics, model artifacts, and the JSON report.

## Tests
```powershell
pytest -q
```

## Limitations
- The included sample dataset is intentionally small and only demonstrates the pipeline; model metrics are not suitable for business decisions.
- Logistic Regression is a baseline classifier. Select the model and evaluation strategy appropriate to the assigned dataset.
- The pipeline assumes a classification target and may need changes for regression or time-series tasks.
- The generated report and MLflow database are local artifacts and are excluded from Git.

## Git tasks
Use the required branch name:
```powershell
git checkout -b feat/w9d5-[name]
git add .
git commit -m "feat: build tracked data analytics experiment pipeline"
git add README.md tests/
git commit -m "test: add pipeline checks and usage documentation"
git push -u origin feat/w9d5-[name]
```
Replace `[name]` with your assigned suffix. Verify with `git log -2 --oneline` and update your PR.
