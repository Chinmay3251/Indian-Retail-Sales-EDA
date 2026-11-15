import numpy as np
import pandas as pd
import pytest
from src.forecasting import prepare_data, make_forecast, evaluate_method

def sample_data(n=48):
    dates = pd.date_range("2021-01-01", periods=n, freq="MS")
    sales = 100 + np.arange(n) * 2 + 8 * np.sin(np.arange(n) * 2 * np.pi / 12)
    return pd.DataFrame({"date": dates, "sales": sales})

def test_prepare_data_sorts_and_deduplicates():
    frame = pd.DataFrame({
        "date": ["2022-02-01", "2022-01-01", "2022-01-01"],
        "sales": [20, 10, 11]
    })
    # Valid input length is deliberately enforced by the preparation function.
    extended = pd.concat([frame, sample_data(12)], ignore_index=True)
    result = prepare_data(extended)
    assert result["date"].is_monotonic_increasing
    assert result["date"].is_unique

def test_naive_forecast_has_requested_horizon():
    data = prepare_data(sample_data())
    result = make_forecast(data, 5, "Naive")
    assert len(result) == 5
    assert np.allclose(result["forecast"], data["sales"].iloc[-1])

def test_holdout_metrics_are_nonnegative():
    data = prepare_data(sample_data())
    result = evaluate_method(data, "Moving Average", window=3)
    assert result["mae"] >= 0
    assert result["rmse"] >= 0

def test_unknown_method_rejected():
    data = prepare_data(sample_data())
    with pytest.raises(ValueError):
        make_forecast(data, 3, "Unknown")
