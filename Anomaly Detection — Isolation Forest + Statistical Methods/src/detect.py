from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def select_features(frame: pd.DataFrame, features: list[str] | None = None) -> list[str]:
    if features:
        missing = [name for name in features if name not in frame.columns]
        if missing:
            raise ValueError(f"Feature columns not found: {missing}")
        selected = features
    else:
        selected = [c for c in frame.select_dtypes(include="number").columns
                    if c.lower() not in {"transaction_id", "id"}]
    if not selected:
        raise ValueError("No numeric feature columns selected.")
    non_numeric = [c for c in selected if not pd.api.types.is_numeric_dtype(frame[c])]
    if non_numeric:
        raise ValueError(f"Features must be numeric: {non_numeric}")
    return selected

def detect_anomalies(frame: pd.DataFrame, features: list[str] | None = None,
                     contamination: float = 0.04, z_threshold: float = 3.0,
                     random_state: int = 42) -> tuple[pd.DataFrame, dict]:
    if frame.empty:
        raise ValueError("Input dataset is empty.")
    if not 0 < contamination <= 0.5:
        raise ValueError("contamination must be greater than 0 and at most 0.5.")
    if z_threshold <= 0:
        raise ValueError("z_threshold must be positive.")

    selected = select_features(frame, features)
    x = frame[selected].apply(pd.to_numeric, errors="coerce")
    x = x.replace([np.inf, -np.inf], np.nan)
    if x.isna().all(axis=None):
        raise ValueError("Selected features contain no usable numeric values.")
    x = x.fillna(x.median()).fillna(0)

    result = frame.copy()
    # Statistical method 1: absolute Z-score, with zero-variance protection.
    means, stds = x.mean(), x.std(ddof=0).replace(0, np.nan)
    z_scores = ((x - means) / stds).abs().fillna(0)
    result["zscore_anomaly"] = z_scores.gt(z_threshold).any(axis=1)

    # Statistical method 2: univariate IQR fences.
    iqr_flags = pd.DataFrame(False, index=x.index, columns=x.columns)
    for col in x.columns:
        q1, q3 = x[col].quantile([0.25, 0.75])
        spread = q3 - q1
        lower, upper = q1 - 1.5 * spread, q3 + 1.5 * spread
        iqr_flags[col] = (x[col] < lower) | (x[col] > upper)
    result["iqr_anomaly"] = iqr_flags.any(axis=1)

    model = IsolationForest(
        n_estimators=200, contamination=contamination,
        random_state=random_state, n_jobs=-1
    )
    result["isolation_forest_anomaly"] = model.fit_predict(x) == -1
    result["any_anomaly"] = result[
        ["zscore_anomaly", "iqr_anomaly", "isolation_forest_anomaly"]
    ].any(axis=1)

    summary = {
        "rows": int(len(result)),
        "features": selected,
        "contamination": float(contamination),
        "z_threshold": float(z_threshold),
        "zscore_anomalies": int(result["zscore_anomaly"].sum()),
        "iqr_anomalies": int(result["iqr_anomaly"].sum()),
        "isolation_forest_anomalies": int(result["isolation_forest_anomaly"].sum()),
        "any_anomalies": int(result["any_anomaly"].sum()),
    }
    return result, summary

def save_outputs(results: pd.DataFrame, summary: dict, features: list[str], output_dir: str | Path):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    results.to_csv(output / "anomaly_results.csv", index=False)
    (output / "summary.json").write_text(json.dumps(summary, indent=2))

    feature = features[0]
    fig, ax = plt.subplots(figsize=(10, 5))
    normal = ~results["isolation_forest_anomaly"]
    ax.scatter(results.loc[normal, feature], results.loc[normal, feature],
               alpha=0.55, label="Not flagged", s=20)
    ax.scatter(results.loc[~normal, feature], results.loc[~normal, feature],
               alpha=0.85, label="Isolation Forest anomaly", s=35)
    ax.set_title(f"Isolation Forest results — {feature}")
    ax.set_xlabel(feature)
    ax.set_ylabel(feature)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output / "anomaly_plot.png", dpi=150)
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Detect anomalies using statistics and Isolation Forest.")
    parser.add_argument("--input", required=True, help="Input CSV file.")
    parser.add_argument("--output", default="outputs")
    parser.add_argument("--features", help="Comma-separated numeric feature columns.")
    parser.add_argument("--contamination", type=float, default=0.04)
    parser.add_argument("--z-threshold", type=float, default=3.0)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    features = [v.strip() for v in args.features.split(",")] if args.features else None
    results, summary = detect_anomalies(frame, features, args.contamination, args.z_threshold)
    chosen = summary["features"]
    save_outputs(results, summary, chosen, args.output)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
