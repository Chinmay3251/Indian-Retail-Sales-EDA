from __future__ import annotations
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

METHODS = ["Naive", "Moving Average", "Holt-Winters"]

def prepare_sales_data(frame: pd.DataFrame) -> pd.DataFrame:
    if not {"date", "sales"}.issubset(frame.columns):
        raise ValueError("Input must contain 'date' and 'sales' columns.")
    data = frame[["date", "sales"]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
    data = data.replace([np.inf, -np.inf], np.nan).dropna()
    data = data.sort_values("date").drop_duplicates("date").reset_index(drop=True)
    if len(data) < 12:
        raise ValueError("At least 12 valid monthly observations are required.")
    return data

def _forecast(train: pd.Series, periods: int, method: str, window: int = 3) -> np.ndarray:
    if periods < 1:
        raise ValueError("Forecast horizon must be at least one period.")
    values = train.astype(float).to_numpy()
    if method == "Naive":
        return np.repeat(values[-1], periods)
    if method == "Moving Average":
        return np.repeat(float(np.mean(values[-min(window, len(values)):])), periods)
    if method == "Holt-Winters":
        if len(values) >= 24:
            model = ExponentialSmoothing(
                values, trend="add", seasonal="add", seasonal_periods=12,
                initialization_method="estimated"
            ).fit(optimized=True)
        else:
            model = ExponentialSmoothing(
                values, trend="add", seasonal=None,
                initialization_method="estimated"
            ).fit(optimized=True)
        return np.asarray(model.forecast(periods), dtype=float)
    raise ValueError(f"Unknown forecasting method: {method}")

def evaluate_models(data: pd.DataFrame, window: int = 3) -> pd.DataFrame:
    split = int(len(data) * 0.8)
    if split < 8 or len(data) - split < 2:
        raise ValueError("Not enough observations for a chronological holdout.")
    train = data["sales"].iloc[:split]
    actual = data["sales"].iloc[split:].to_numpy(dtype=float)
    rows = []
    for method in METHODS:
        try:
            predicted = _forecast(train, len(actual), method, window)
            error = actual - predicted
            rows.append({
                "method": method,
                "mae": float(np.mean(np.abs(error))),
                "rmse": float(np.sqrt(np.mean(error ** 2))),
                "train_rows": len(train),
                "test_rows": len(actual),
            })
        except (ValueError, np.linalg.LinAlgError) as exc:
            rows.append({"method": method, "mae": np.nan, "rmse": np.nan,
                         "train_rows": len(train), "test_rows": len(actual),
                         "error": str(exc)})
    return pd.DataFrame(rows)

def build_forecast(data: pd.DataFrame, horizon: int, method: str, window: int = 3) -> pd.DataFrame:
    values = _forecast(data["sales"], horizon, method, window)
    dates = data["date"]
    freq = pd.infer_freq(dates)
    if freq is None:
        # Monthly data default to month-start; daily/other data fallback to inferred median gap.
        gaps = dates.diff().dropna().dt.days
        median_gap = int(gaps.median()) if not gaps.empty else 30
        freq = "MS" if 25 <= median_gap <= 35 else f"{max(1, median_gap)}D"
    future_dates = pd.date_range(start=dates.iloc[-1], periods=horizon + 1, freq=freq)[1:]
    return pd.DataFrame({"date": future_dates, "forecast": values})

def make_history_figure(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.date, y=data.sales, mode="lines+markers",
                             name="Historical sales"))
    fig.update_layout(title="Historical Sales Trend", xaxis_title="Date",
                      yaxis_title="Sales", hovermode="x unified",
                      template="plotly_white")
    return fig

def make_forecast_figure(data: pd.DataFrame, forecast: pd.DataFrame, method: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.date, y=data.sales, mode="lines+markers",
                             name="Actual sales"))
    fig.add_trace(go.Scatter(x=forecast.date, y=forecast.forecast,
                             mode="lines+markers", name=f"{method} forecast",
                             line=dict(dash="dash")))
    fig.update_layout(title="Sales Forecast", xaxis_title="Date",
                      yaxis_title="Sales", hovermode="x unified",
                      template="plotly_white")
    return fig

def save_pipeline_outputs(data: pd.DataFrame, forecast: pd.DataFrame,
                          comparison: pd.DataFrame, method: str, output_dir: str | Path):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(out / "sales_forecast.csv", index=False)
    comparison.to_csv(out / "model_comparison.csv", index=False)
    fig = make_forecast_figure(data, forecast, method)
    fig.write_html(out / "sales_forecast.html", include_plotlyjs="cdn")
    valid = comparison.dropna(subset=["rmse"])
    summary = {
        "observations": int(len(data)),
        "last_observed_date": str(data.date.iloc[-1].date()),
        "selected_method": method,
        "forecast_periods": int(len(forecast)),
        "best_holdout_method": str(valid.sort_values("rmse").iloc[0].method) if not valid.empty else None,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary

def main():
    parser = argparse.ArgumentParser(description="End-to-end sales forecasting pipeline.")
    parser.add_argument("--input", default="data/monthly_sales.csv")
    parser.add_argument("--horizon", type=int, default=6)
    parser.add_argument("--method", choices=METHODS, default=None)
    parser.add_argument("--window", type=int, default=3)
    parser.add_argument("--output", default="outputs")
    args = parser.parse_args()
    data = prepare_sales_data(pd.read_csv(args.input))
    comparison = evaluate_models(data, args.window)
    valid = comparison.dropna(subset=["rmse"])
    selected = args.method or str(valid.sort_values("rmse").iloc[0].method)
    forecast = build_forecast(data, args.horizon, selected, args.window)
    summary = save_pipeline_outputs(data, forecast, comparison, selected, args.output)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
