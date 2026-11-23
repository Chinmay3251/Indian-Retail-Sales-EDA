from pathlib import Path
import duckdb
csv=Path("data/sales_100k.csv").resolve().as_posix()
q=[("Revenue by region",f"SELECT region,ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) revenue FROM read_csv_auto('{csv}') GROUP BY region ORDER BY revenue DESC"),("Monthly revenue",f"SELECT DATE_TRUNC('month',CAST(order_date AS DATE)) month,ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) revenue FROM read_csv_auto('{csv}') GROUP BY month ORDER BY month"),("Top products",f"SELECT product,SUM(quantity) units,ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) revenue FROM read_csv_auto('{csv}') GROUP BY product ORDER BY revenue DESC LIMIT 10"),("Channel performance",f"SELECT channel,COUNT(*) orders,ROUND(AVG(quantity*unit_price*(1-discount_pct)),2) avg_order_value FROM read_csv_auto('{csv}') GROUP BY channel ORDER BY avg_order_value DESC"),("Top customers",f"SELECT customer_id,COUNT(*) orders,ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) revenue FROM read_csv_auto('{csv}') GROUP BY customer_id ORDER BY revenue DESC LIMIT 20")]
with duckdb.connect() as con:
 for title,sql in q:
  print("\n---",title,"---")
  print(con.execute(sql).fetchdf().to_string(index=False))
