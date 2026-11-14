# W9D2 — MLflow Model Registry for Analyst Models

## Objective
Train a baseline analyst classification model, track its experiment, register the trained model, assign a `champion` alias, and load the registered model for inference.

## Project files
- `src/train_register.py` — creates a reproducible sample churn dataset, trains Logistic Regression, logs parameters/metrics/model, registers a model version, and assigns the `champion` alias.
- `src/predict_registered.py` — loads the registered model through its alias and predicts a sample row.
- `tests/test_model_registry.py` — validates the generated training dataset.
- `requirements.txt` — project dependencies.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Train and register
Run from the project root:
```powershell
python src/train_register.py
```
The project uses a local SQLite tracking/registry database (`mlflow.db`) so the Model Registry is backed by a database store.

## Open MLflow UI
In a second PowerShell terminal:
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Open `http://127.0.0.1:5000`. Select the experiment and inspect the run parameters, metrics, and registered model.

## Load and predict using the registered alias
After the training script has completed:
```powershell
python src/predict_registered.py
```

## What is logged?
- Parameters: model type, iteration limit, test split, random seed, and feature count.
- Metrics: accuracy, precision, recall, and F1 score.
- Model: serialized scikit-learn model with inferred signature and input example.
- Registry: model name `AnalystChurnModel`, version, and `champion` alias.

## Test
```powershell
pytest -q
```

## Notes and limitations
- The included data is synthetic and is only for demonstrating registry workflow. Replace it with the assigned analyst dataset before reporting business performance.
- The example is a baseline Logistic Regression classifier, not a production-ready churn model.
- The `champion` alias is updated to the newly registered version each time the training script runs.
- Keep `mlflow.db` and `mlruns/` out of Git; they are generated locally.

## Git workflow
Use the required branch name:
```powershell
git checkout -b feat/w9d2-[name]
git add .
git commit -m "feat: train and register analyst model with MLflow"
git add README.md tests/
git commit -m "docs: document MLflow model registry workflow"
git push -u origin feat/w9d2-[name]
```
Replace `[name]` with your assigned suffix. Verify with `git log -2 --oneline`, then update your PR.
