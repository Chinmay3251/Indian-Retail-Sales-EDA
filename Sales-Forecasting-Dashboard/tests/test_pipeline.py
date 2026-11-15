import numpy as np
import pandas as pd
import pytest
from src.pipeline import prepare_sales_data, build_forecast, evaluate_models, METHODS

def sample_data(n=60):
    dates = pd.date_range("2020-01-01", periods=n, freq="MS")
    values = 500 + np.arange(n) * 4 + 30 * np.sin(np.arange(n) * 2 * np.pi / 12)
    return pd.DataFrame({"date": dates, "sales": values})

def test_prepare_sales_data_cleans_and_sorts():
    frame = pd.DataFrame({
        "date": ["2021-02-01", "2021-01-01", "2021-01-01", "bad"],
        "sales": [20, 10, 11, 5],
    })
    frame = pd.concat([frame, sample_data(12)], ignore_index=True)
    result = prepare_sales_data(frame)
    assert result.date.is_monotonic_increasing
    assert result.date.is_unique
    assert result.sales.notna().all()

def test_build_forecast_returns_horizon():
    data = prepare_sales_data(sample_data())
    result = build_forecast(data, 6, "Naive")
    assert len(result) == 6
    assert np.allclose(result.forecast, data.sales.iloc[-1])

def test_model_comparison_contains_all_methods():
    data = prepare_sales_data(sample_data())
    result = evaluate_models(data)
    assert set(result.method) == set(METHODS)
    assert (result.rmse.dropna() >= 0).all()

def test_invalid_horizon_rejected():
    data = prepare_sales_data(sample_data())
    with pytest.raises(ValueError):
        build_forecast(data, 0, "Naive")
