import pandas as pd
import pytest
from src.analysis import analyze,load_series

def test_load_series(tmp_path):
    p=tmp_path/"x.csv"
    pd.DataFrame({"date":pd.date_range("2020-01-01",periods=24,freq="MS"),"sales":range(24)}).to_csv(p,index=False)
    assert len(load_series(p,"date","sales","MS"))==24

def test_arima_metrics_and_forecast():
    idx=pd.date_range("2020-01-01",periods=36,freq="MS")
    s=pd.Series([100+i+5*((i%12)/12) for i in range(36)],index=idx)
    report,*_=analyze(s,test_size=4)
    assert report["mae"]>=0 and report["rmse"]>=0 and len(report["forecast"])==4

def test_short_series_rejected():
    s=pd.Series(range(6),index=pd.date_range("2020-01-01",periods=6,freq="MS"))
    with pytest.raises(ValueError): analyze(s,test_size=3)
