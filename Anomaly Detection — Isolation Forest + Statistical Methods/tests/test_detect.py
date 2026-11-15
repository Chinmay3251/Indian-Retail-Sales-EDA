import pandas as pd
import pytest
from src.detect import detect_anomalies, select_features

def test_detection_adds_all_method_flags():
    frame = pd.DataFrame({
        "transaction_id": range(1, 81),
        "amount": [100.0] * 78 + [1200.0, 1500.0],
        "items": [2] * 80,
    })
    result, summary = detect_anomalies(frame, ["amount", "items"], contamination=0.05)
    for col in ["zscore_anomaly", "iqr_anomaly", "isolation_forest_anomaly", "any_anomaly"]:
        assert col in result.columns
    assert summary["rows"] == 80
    assert result["isolation_forest_anomaly"].sum() >= 1

def test_rejects_missing_feature():
    with pytest.raises(ValueError):
        select_features(pd.DataFrame({"amount": [1, 2]}), ["missing"])

def test_rejects_invalid_contamination():
    frame = pd.DataFrame({"amount": list(range(40))})
    with pytest.raises(ValueError):
        detect_anomalies(frame, ["amount"], contamination=0)
