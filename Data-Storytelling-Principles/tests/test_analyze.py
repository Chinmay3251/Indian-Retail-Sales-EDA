import pandas as pd
import pytest
from src.analyze import load_data

def test_missing_columns_raise_error(tmp_path):
    p=tmp_path/"bad.csv"
    pd.DataFrame({"date":["2025-01-01"],"sales":[2]}).to_csv(p,index=False)
    with pytest.raises(ValueError): load_data(p)

def test_valid_data_loads(tmp_path):
    df=pd.DataFrame({"order_id":[1],"order_date":["2025-01-01"],"category":["A"],"region":["North"],
                     "sales":[100],"profit":[20],"quantity":[2],"discount":[.1]})
    p=tmp_path/"good.csv"; df.to_csv(p,index=False)
    assert len(load_data(p))==1
