from pathlib import Path
import pandas as pd
DATA=Path(__file__).resolve().parents[1]/"data/indian_retail_sales.csv"
def test_rows_and_unique_order_ids():
 df=pd.read_csv(DATA); assert len(df)==5000; assert df.order_id.is_unique
def test_expected_columns_and_nonnegative_sales():
 df=pd.read_csv(DATA); assert {"order_date","city","category","net_sales_inr","order_status"}.issubset(df.columns); assert (df.net_sales_inr>=0).all()
