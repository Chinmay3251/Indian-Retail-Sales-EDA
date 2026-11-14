import pandas as pd
import pytest
from src.ab_test_tracking import analyze_ab_test

def sample():
    return pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6],
        "variant": ["control", "control", "control", "treatment", "treatment", "treatment"],
        "converted": [0, 1, 0, 1, 1, 0],
        "revenue": [0, 50, 0, 60, 70, 0],
    })

def test_analyze_returns_both_variants_and_statistics():
    result = analyze_ab_test(sample())
    assert result["control"]["users"] == 3
    assert result["treatment"]["users"] == 3
    assert "p_value_two_sided" in result
    assert 0 <= result["p_value_two_sided"] <= 1

def test_rejects_missing_variant():
    df = sample()
    df.loc[df["variant"] == "treatment", "variant"] = "control"
    with pytest.raises(ValueError):
        analyze_ab_test(df)

def test_rejects_invalid_conversion_values():
    df = sample()
    df.loc[0, "converted"] = 2
    with pytest.raises(ValueError):
        analyze_ab_test(df)
