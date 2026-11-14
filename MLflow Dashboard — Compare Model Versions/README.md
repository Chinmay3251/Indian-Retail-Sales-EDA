# W9D4 — MLflow Dashboard: Compare Model Versions

## Objective
Build a Streamlit dashboard that connects to an MLflow Model Registry and compares registered model versions using their run metrics, parameters, aliases, and metadata.

## Features
- Connect to a configurable MLflow Tracking URI.
- List registered models and select a model.
- Display available versions, status, creation time, run ID, aliases, and descriptions.
- Select versions for side-by-side comparison.
- Visualize a selected logged metric across versions.
- Inspect parameters, tags, source, and version metadata.
- Refresh registry information.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Start the MLflow tracking UI
Use the same backend store that contains the registered model versions. For the local SQLite database used in the W9D2 example:
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Keep this terminal running.

## Start the dashboard
Open a second PowerShell terminal in the project root:
```powershell
$env:MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"
streamlit run app/dashboard.py
```
Open the Streamlit URL shown in the terminal (normally `http://localhost:8501`).

If your registry uses a remote tracking server, set its URI instead:
```powershell
$env:MLFLOW_TRACKING_URI = "http://localhost:5000"
```
The URI must point to the same MLflow backend where model versions were registered. A separate empty database will show no models.

## Usage
1. Select a registered model.
2. Review the version list and aliases.
3. Select two or more versions in **Select versions to compare**.
4. Choose a metric to visualize.
5. Compare the run metrics and parameters in the table.
6. Select a version to inspect its parameters, tags, and registry metadata.

## Test
```powershell
pytest -q
```

## Notes and limitations
- The dashboard reads registered model versions and their source runs; it does not train, register, promote, or delete models.
- Only metrics logged to the source run can be compared.
- Model versions whose source run is unavailable may show blank metrics/parameters.
- MLflow registry availability depends on the configured backend store and permissions.
- This is a local development dashboard; configure authentication and network security before exposing a remote tracking server.

## Git workflow
```powershell
git checkout -b feat/w9d4-[name]
git add .
git commit -m "feat: add MLflow model version comparison dashboard"
git add README.md tests/
git commit -m "test: add dashboard helper tests and usage documentation"
git push -u origin feat/w9d4-[name]
```
Replace `[name]` with your assigned suffix. Verify with `git log -2 --oneline` and update your PR.
