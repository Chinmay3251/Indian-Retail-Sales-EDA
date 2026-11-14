"""End-to-end tracked data analytics experiment pipeline using MLflow."""
from pathlib import Path
import argparse
import json
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACKING_URI = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

def load_data(csv_path: Path, target: str):
    df = pd.read_csv(csv_path)
    if df.empty:
        raise ValueError("Dataset has no rows.")
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' was not found.")
    df = df.dropna(subset=[target])
    if df[target].nunique() < 2:
        raise ValueError("Classification target must contain at least two classes.")
    X = df.drop(columns=[target])
    y = df[target]
    if X.empty:
        raise ValueError("Dataset must contain at least one feature column.")
    return df, X, y

def build_model(X: pd.DataFrame):
    numeric_cols = X.select_dtypes(include="number").columns.tolist()
    categorical_cols = [c for c in X.columns if c not in numeric_cols]
    transformers = []
    if numeric_cols:
        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        transformers.append(("numeric", numeric_pipe, numeric_cols))
    if categorical_cols:
        categorical_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ])
        transformers.append(("categorical", categorical_pipe, categorical_cols))
    preprocessor = ColumnTransformer(transformers=transformers)
    return Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ])

def run_pipeline(csv_path: Path, target: str, experiment_name: str,
                 run_name: str, tracking_uri: str = DEFAULT_TRACKING_URI):
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    df, X, y = load_data(csv_path, target)

    stratify = y if y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=stratify
    )
    model = build_model(X_train)

    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params({
            "dataset": csv_path.name,
            "target": target,
            "rows": len(df),
            "features": X.shape[1],
            "train_rows": len(X_train),
            "test_rows": len(X_test),
            "model": "LogisticRegression",
            "test_size": 0.25,
            "random_state": 42
        })
        mlflow.log_metric("missing_cells", int(df.isna().sum().sum()))
        mlflow.log_metric("duplicate_rows", int(df.duplicated().sum()))

        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision_weighted": precision_score(y_test, predictions, average="weighted", zero_division=0),
            "recall_weighted": recall_score(y_test, predictions, average="weighted", zero_division=0),
            "f1_weighted": f1_score(y_test, predictions, average="weighted", zero_division=0)
        }
        if hasattr(model, "predict_proba") and y.nunique() == 2:
            try:
                metrics["roc_auc"] = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
            except ValueError:
                pass
        mlflow.log_metrics({k: float(v) for k, v in metrics.items()})

        signature = infer_signature(X_train, model.predict(X_train))
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            signature=signature,
            input_example=X_train.head(3)
        )

        report = {
            "run_id": run.info.run_id,
            "experiment": experiment_name,
            "dataset": csv_path.name,
            "target": target,
            "rows": len(df),
            "columns": list(df.columns),
            "metrics": {k: float(v) for k, v in metrics.items()},
            "data_quality": {
                "missing_cells": int(df.isna().sum().sum()),
                "duplicate_rows": int(df.duplicated().sum())
            }
        }
        report_path = ROOT / "artifacts" / "experiment_report.json"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        mlflow.log_artifact(str(report_path), artifact_path="reports")
        print(json.dumps(report, indent=2))
        return report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(ROOT/"data"/"sample_customer_churn.csv"))
    parser.add_argument("--target", default="churn")
    parser.add_argument("--experiment", default="W9D5-Tracked-Analytics-Pipeline")
    parser.add_argument("--run-name", default="baseline-logistic-regression")
    parser.add_argument("--tracking-uri", default=DEFAULT_TRACKING_URI)
    args = parser.parse_args()
    run_pipeline(Path(args.csv), args.target, args.experiment, args.run_name, args.tracking_uri)

if __name__ == "__main__":
    main()
