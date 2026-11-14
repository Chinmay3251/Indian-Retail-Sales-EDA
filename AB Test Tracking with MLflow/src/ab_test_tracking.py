"""Analyze an A/B test and track variants and results with MLflow."""
from pathlib import Path
import argparse
import json
import math
import pandas as pd
import mlflow

ROOT = Path(__file__).resolve().parents[1]
TRACKING_URI = f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"

REQUIRED_COLUMNS = {"user_id", "variant", "converted", "revenue"}

def analyze_ab_test(df: pd.DataFrame) -> dict:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    data = df.copy()
    data["variant"] = data["variant"].astype(str).str.lower()
    data["converted"] = pd.to_numeric(data["converted"], errors="coerce")
    data["revenue"] = pd.to_numeric(data["revenue"], errors="coerce")
    data = data.dropna(subset=["variant", "converted", "revenue"])
    if not set(data["variant"].unique()).issubset({"control", "treatment"}):
        raise ValueError("variant must contain only 'control' and 'treatment'.")
    if not {"control", "treatment"}.issubset(set(data["variant"].unique())):
        raise ValueError("Both control and treatment variants are required.")
    if not data["converted"].isin([0, 1]).all():
        raise ValueError("converted must contain only 0 or 1.")

    groups = {}
    for name in ("control", "treatment"):
        part = data[data["variant"] == name]
        groups[name] = {
            "users": int(len(part)),
            "conversions": int(part["converted"].sum()),
            "conversion_rate": float(part["converted"].mean()),
            "average_revenue": float(part["revenue"].mean()),
            "total_revenue": float(part["revenue"].sum()),
        }

    c, t = groups["control"], groups["treatment"]
    uplift = ((t["conversion_rate"] - c["conversion_rate"]) / c["conversion_rate"]
              if c["conversion_rate"] else None)
    # Two-proportion z-test, pooled standard error.
    p_pool = (c["conversions"] + t["conversions"]) / (c["users"] + t["users"])
    se = math.sqrt(p_pool * (1-p_pool) * (1/c["users"] + 1/t["users"]))
    z_score = ((t["conversion_rate"] - c["conversion_rate"]) / se) if se else 0.0
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    return {
        "control": c,
        "treatment": t,
        "conversion_rate_absolute_difference": t["conversion_rate"] - c["conversion_rate"],
        "conversion_rate_relative_uplift": uplift,
        "z_score": z_score,
        "p_value_two_sided": p_value,
        "statistically_significant_at_0_05": bool(p_value < 0.05),
    }

def track_experiment(csv_path: Path, experiment_name: str):
    df = pd.read_csv(csv_path)
    results = analyze_ab_test(df)
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name="ab-test-comparison") as parent:
        mlflow.log_param("dataset", csv_path.name)
        mlflow.log_param("test_type", "two_proportion_z_test")
        mlflow.log_param("control_variant", "control")
        mlflow.log_param("treatment_variant", "treatment")
        mlflow.log_param("significance_threshold", 0.05)
        mlflow.log_metric("conversion_rate_absolute_difference",
                          results["conversion_rate_absolute_difference"])
        mlflow.log_metric("z_score", results["z_score"])
        mlflow.log_metric("p_value_two_sided", results["p_value_two_sided"])
        mlflow.log_metric("statistically_significant_at_0_05",
                          int(results["statistically_significant_at_0_05"]))
        if results["conversion_rate_relative_uplift"] is not None:
            mlflow.log_metric("conversion_rate_relative_uplift",
                              results["conversion_rate_relative_uplift"])

        for variant in ("control", "treatment"):
            metrics = results[variant]
            with mlflow.start_run(run_name=f"{variant}-variant", nested=True):
                mlflow.log_param("variant", variant)
                mlflow.log_metric("users", metrics["users"])
                mlflow.log_metric("conversions", metrics["conversions"])
                mlflow.log_metric("conversion_rate", metrics["conversion_rate"])
                mlflow.log_metric("average_revenue", metrics["average_revenue"])
                mlflow.log_metric("total_revenue", metrics["total_revenue"])

        artifact_dir = ROOT / "artifacts"
        artifact_dir.mkdir(exist_ok=True)
        report_file = artifact_dir / "ab_test_results.json"
        report_file.write_text(json.dumps(results, indent=2), encoding="utf-8")
        mlflow.log_artifact(str(report_file), artifact_path="reports")
        print(json.dumps(results, indent=2))
        print("Parent MLflow run ID:", parent.info.run_id)
        return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=str(ROOT / "data" / "sample_ab_test.csv"))
    parser.add_argument("--experiment", default="W9D3-AB-Test-Tracking")
    args = parser.parse_args()
    track_experiment(Path(args.csv), args.experiment)

if __name__ == "__main__":
    main()
