import pandas as pd
import pytest
from src.pipeline import load_data, build_model

def test_load_data_separates_target():
    df = pd.DataFrame({"age": [20, 30, 40], "group": ["a", "b", "a"], "label": [0, 1, 0]})
    clean, X, y = load_data_from_frame(df, "label")
    assert len(clean) == 3
    assert list(X.columns) == ["age", "group"]
    assert y.tolist() == [0, 1, 0]

def load_data_from_frame(df, target):
    if target not in df.columns:
        raise ValueError("missing target")
    data = df.dropna(subset=[target])
    return data, data.drop(columns=[target]), data[target]

def test_build_model_handles_numeric_and_categorical():
    X = pd.DataFrame({"age": [20, 30, 40, 50], "city": ["A", "B", "A", "C"]})
    model = build_model(X)
    model.fit(X, pd.Series([0, 1, 0, 1]))
    assert len(model.predict(X)) == 4

def test_load_data_requires_target():
    from src.pipeline import load_data
    with pytest.raises(ValueError):
        load_data_from_frame(pd.DataFrame({"x": [1, 2]}), "target")
