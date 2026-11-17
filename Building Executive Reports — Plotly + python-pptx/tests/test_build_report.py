import pandas as pd
import pytest
from src.build_report import load_data, calculate_kpis

def test_missing_columns_rejected(tmp_path):
    p=tmp_path/'bad.csv'
    pd.DataFrame({'month':['2025-01-01']}).to_csv(p,index=False)
    with pytest.raises(ValueError): load_data(p)

def test_kpi_totals():
    d=pd.DataFrame({'month':pd.to_datetime(['2025-01-01','2025-02-01']),
      'category':['A','A'],'revenue':[100.,120.],'profit':[20.,30.],'orders':[2,3]})
    k,m,c=calculate_kpis(d)
    assert k['total_revenue']==220
    assert k['total_profit']==50
    assert k['total_orders']==5
    assert k['top_category']=='A'
