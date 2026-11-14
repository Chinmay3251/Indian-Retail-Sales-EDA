"""Train a simple analyst model and register it in MLflow Model Registry."""
from pathlib import Path
import argparse
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
TRACKING_DB = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

def build_dataset():
    X, y = make_classification(
        n_samples=600, n_features=6, n_informative=4, n_redundant=1,
        n_classes=2, weights=[0.65, 0.35], random_state=42
    )
    columns = ["tenure_months", "monthly_spend", "support_tickets",
               "usage_score", "late_payments", "plan_changes"]
    frame = pd.DataFrame(X, columns=columns)
    frame["churn"] = y
    return frame

def train_and_register(experiment_name="W9D2-Analyst-Model-Registry",
                       registered_model_name="AnalystChurnModel"):
    mlflow.set_tracking_uri(TRACKING_DB)
    mlflow.set_registry_uri(TRACKING_DB)
    mlflow.set_experiment(experiment_name)

    df = build_dataset()
    X = df.drop(columns=["churn"])
    y = df["churn"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=42)
    with mlflow.start_run(run_name="logistic-regression-baseline") as run:
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)

        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "precision": precision_score(y_test, predictions, zero_division=0),
            "recall": recall_score(y_test, predictions, zero_division=0),
            "f1_score": f1_score(y_test, predictions, zero_division=0),
        }
        mlflow.log_params({
            "model_type": "LogisticRegression",
            "max_iter": 1000,
            "test_size": 0.2,
            "random_state": 42,
            "feature_count": X.shape[1],
        })
        mlflow.log_metrics(metrics)

        signature = infer_signature(X_train, model.predict(X_train))
        model_info = mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="analyst_model",
            signature=signature,
            input_example=X_train.head(3),
            registered_model_name=registered_model_name,
        )

        client = mlflow.tracking.MlflowClient()
        version = client.get_latest_versions(registered_model_name)[0]
        client.set_registered_model_alias(registered_model_name, "champion", version.version)

        print("Run ID:", run.info.run_id)
        print("Registered model:", registered_model_name)
        print("Model version:", version.version)
        print("Model URI:", model_info.model_uri)
        print("Champion alias: champion")
        print("Metrics:", metrics)
        return registered_model_name, version.version, metrics

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", default="W9D2-Analyst-Model-Registry")
    parser.add_argument("--model-name", default="AnalystChurnModel")
    args = parser.parse_args()
    train_and_register(args.experiment, args.model_name)

if __name__ == "__main__":
    main()
