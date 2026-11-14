from pathlib import Path
import argparse, json
import pandas as pd
import mlflow

ROOT = Path(__file__).resolve().parents[1]

def run(csv, experiment, run_name):
    df = pd.read_csv(csv)
    if df.empty: raise ValueError("CSV has no data rows")
    numeric = df.select_dtypes(include="number")
    missing = int(df.isna().sum().sum())
    total = int(df.size)
    report = {
        "rows": int(len(df)), "columns": int(len(df.columns)),
        "numeric_columns": int(len(numeric.columns)),
        "categorical_columns": int(len(df.columns)-len(numeric.columns)),
        "missing_cells": missing, "missing_rate": missing/total if total else 0,
        "duplicate_rows": int(df.duplicated().sum())
    }
    mlflow.set_experiment(experiment)
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("dataset", Path(csv).name)
        mlflow.log_param("analysis_type", "csv_data_profile")
        mlflow.log_param("row_count", len(df))
        mlflow.log_param("column_count", len(df.columns))
        for key in ("numeric_columns","categorical_columns","missing_cells","missing_rate","duplicate_rows"):
            mlflow.log_metric(key, report[key])
        out = ROOT/"artifacts"; out.mkdir(exist_ok=True)
        j = out/"data_profile.json"; j.write_text(json.dumps(report, indent=2))
        mlflow.log_artifact(str(j), "reports")
        if not numeric.empty:
            c = out/"numeric_summary.csv"; numeric.describe().to_csv(c)
            mlflow.log_artifact(str(c), "reports")
        print(json.dumps(report, indent=2))
        print("MLflow run:", mlflow.active_run().info.run_id)

if __name__ == "__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--csv", default=str(ROOT/"data"/"sample_sales.csv"))
    p.add_argument("--experiment", default="W9D1-Data-Analytics-Experiments")
    p.add_argument("--run-name", default="csv-data-profile")
    a=p.parse_args(); run(a.csv,a.experiment,a.run_name)
