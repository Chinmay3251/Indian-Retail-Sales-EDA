import pandas as pd
import pytest
from src.data import prepare_market_data

def test_adjusted_close_preferred():
    f=pd.DataFrame({"Date":pd.date_range("2024-01-01",periods=35),"Close":[101]*35,"Adj Close":[100]*35})
    got=prepare_market_data(f)
    assert list(got.columns)==["ds","y"] and len(got)==35 and got.y.iloc[0]==100

def test_rejects_short_data():
    f=pd.DataFrame({"Date":pd.date_range("2024-01-01",periods=10),"Close":[100]*10})
    with pytest.raises(ValueError): prepare_market_data(f)
