"""Load the registered champion model and run a sample prediction."""
from pathlib import Path
import mlflow
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TRACKING_DB = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

def predict():
    mlflow.set_tracking_uri(TRACKING_DB)
    mlflow.set_registry_uri(TRACKING_DB)
    model = mlflow.pyfunc.load_model("models:/AnalystChurnModel@champion")
    sample = pd.DataFrame([{
        "tenure_months": 0.2,
        "monthly_spend": -0.4,
        "support_tickets": 1.1,
        "usage_score": -0.7,
        "late_payments": 0.8,
        "plan_changes": 0.3,
    }])
    print("Predicted churn class:", model.predict(sample).tolist())

if __name__ == "__main__":
    predict()
