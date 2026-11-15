from __future__ import annotations
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

METHODS = ["Naive", "Moving Average", "Exponential Smoothing"]

def prepare_data(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"date", "sales"}
    if not required.issubset(frame.columns):
        raise ValueError("CSV must contain 'date' and 'sales' columns.")
    data = frame[["date", "sales"]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
    data = data.dropna().sort_values("date").drop_duplicates("date").reset_index(drop=True)
    if len(data) < 12:
        raise ValueError("At least 12 valid observations are required.")
    if not np.isfinite(data["sales"]).all():
        raise ValueError("Sales values must be finite.")
    return data

def _fit_predict(train: pd.Series, horizon: int, method: str, window: int = 3) -> np.ndarray:
    if horizon < 1:
        raise ValueError("Forecast horizon must be at least 1.")
    values = train.astype(float).to_numpy()
    if method == "Naive":
        return np.repeat(values[-1], horizon)
    if method == "Moving Average":
        return np.repeat(float(np.mean(values[-min(window, len(values)):])), horizon)
    if method == "Exponential Smoothing":
        if len(values) < 12:
            raise ValueError("Exponential Smoothing requires at least 12 training observations.")
        fitted = ExponentialSmoothing(
            values, trend="add", seasonal=None, initialization_method="estimated"
        ).fit(optimized=True)
        return np.asarray(fitted.forecast(horizon), dtype=float)
    raise ValueError(f"Unknown forecasting method: {method}")

def evaluate_method(data: pd.DataFrame, method: str, window: int = 3) -> dict:
    split = int(len(data) * 0.8)
    if split < 8 or len(data) - split < 2:
        raise ValueError("Not enough data for chronological holdout evaluation.")
    train = data["sales"].iloc[:split]
    test = data["sales"].iloc[split:]
    predictions = _fit_predict(train, len(test), method, window)
    errors = test.to_numpy(dtype=float) - predictions
    return {
        "method": method,
        "mae": float(np.mean(np.abs(errors))),
        "rmse": float(np.sqrt(np.mean(errors ** 2))),
        "train_observations": int(len(train)),
        "test_observations": int(len(test)),
    }

def make_forecast(data: pd.DataFrame, horizon: int, method: str, window: int = 3) -> pd.DataFrame:
    values = _fit_predict(data["sales"], horizon, method, window)
    if pd.api.types.is_datetime64_any_dtype(data["date"]):
        freq = pd.infer_freq(data["date"])
    else:
        freq = None
    if freq is None:
        freq = "MS"
    future_dates = pd.date_range(
        start=data["date"].iloc[-1], periods=horizon + 1, freq=freq
    )[1:]
    return pd.DataFrame({"date": future_dates, "forecast": values})
