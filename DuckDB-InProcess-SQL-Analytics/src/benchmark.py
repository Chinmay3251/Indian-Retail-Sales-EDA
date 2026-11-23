"""DuckDB/Pandas benchmark: same CSV, three equivalent queries, five runs each."""
from pathlib import Path
import statistics,time
import duckdb,pandas as pd
CSV=Path("data/sales_100k.csv").resolve(); N=5
SQL={"revenue_by_region":f"SELECT region,SUM(quantity*unit_price*(1-discount_pct)) net_revenue FROM read_csv_auto('{CSV.as_posix()}') GROUP BY region ORDER BY net_revenue DESC","monthly_revenue":f"SELECT DATE_TRUNC('month',CAST(order_date AS DATE)) sales_month,SUM(quantity*unit_price*(1-discount_pct)) net_revenue FROM read_csv_auto('{CSV.as_posix()}') GROUP BY sales_month ORDER BY sales_month","top_products":f"SELECT product,SUM(quantity) units_sold,SUM(quantity*unit_price*(1-discount_pct)) net_revenue FROM read_csv_auto('{CSV.as_posix()}') GROUP BY product ORDER BY net_revenue DESC LIMIT 10"}
def pandas_q(df,name):
 net=df.quantity*df.unit_price*(1-df.discount_pct)
 if name=="revenue_by_region": return df.assign(net_revenue=net).groupby("region",as_index=False).net_revenue.sum().sort_values("net_revenue",ascending=False)
 if name=="monthly_revenue": return df.assign(sales_month=pd.to_datetime(df.order_date).dt.to_period("M").astype(str),net_revenue=net).groupby("sales_month",as_index=False).net_revenue.sum().sort_values("sales_month")
 return df.assign(net_revenue=net).groupby("product",as_index=False).agg(units_sold=("quantity","sum"),net_revenue=("net_revenue","sum")).sort_values("net_revenue",ascending=False).head(10)
def main():
 rows=[]
 for name,sql in SQL.items():
  dt=[]
  for _ in range(N):
   t=time.perf_counter()
   with duckdb.connect() as c:c.execute(sql).fetchdf()
   dt.append(time.perf_counter()-t)
  pt=[]
  for _ in range(N):
   t=time.perf_counter(); df=pd.read_csv(CSV); pandas_q(df,name); pt.append(time.perf_counter()-t)
  d=statistics.median(dt); p=statistics.median(pt)
  rows.append({"query":name,"duckdb_median_seconds":round(d,6),"pandas_median_seconds":round(p,6),"pandas_over_duckdb_speedup":round(p/d,3) if d else None,"repeats":N,"rows":len(df)})
 out=pd.DataFrame(rows); Path("reports").mkdir(exist_ok=True); out.to_csv("reports/benchmark_results.csv",index=False); print(out.to_string(index=False)); print("Saved reports/benchmark_results.csv")
if __name__=="__main__":main()
