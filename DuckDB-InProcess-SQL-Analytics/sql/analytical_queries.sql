-- Five analytical SQL queries. Run with DuckDB; CSV path is relative to project root.
-- 1 Revenue by region
SELECT region, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) net_revenue FROM read_csv_auto('data/sales_100k.csv') GROUP BY region ORDER BY net_revenue DESC;
-- 2 Monthly revenue trend
SELECT DATE_TRUNC('month',CAST(order_date AS DATE)) sales_month, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) net_revenue FROM read_csv_auto('data/sales_100k.csv') GROUP BY sales_month ORDER BY sales_month;
-- 3 Top products
SELECT product, SUM(quantity) units_sold, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) net_revenue FROM read_csv_auto('data/sales_100k.csv') GROUP BY product ORDER BY net_revenue DESC LIMIT 10;
-- 4 Channel performance
SELECT channel, COUNT(*) orders, ROUND(AVG(quantity*unit_price*(1-discount_pct)),2) avg_order_value FROM read_csv_auto('data/sales_100k.csv') GROUP BY channel ORDER BY avg_order_value DESC;
-- 5 Top customers
SELECT customer_id, COUNT(*) order_count, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) customer_revenue FROM read_csv_auto('data/sales_100k.csv') GROUP BY customer_id ORDER BY customer_revenue DESC LIMIT 20;
