-- Bar
SELECT category, SUM(revenue) total_revenue FROM sales GROUP BY category ORDER BY 2 DESC;
-- Line
SELECT DATE_TRUNC('month',order_date)::date month, SUM(revenue) total_revenue FROM sales GROUP BY 1 ORDER BY 1;
-- Pie
SELECT category, SUM(revenue) total_revenue FROM sales GROUP BY category;
-- Table
SELECT product,category,region,SUM(quantity) units,SUM(revenue) revenue,SUM(profit) profit FROM sales GROUP BY 1,2,3 ORDER BY 5 DESC;
-- Metric
SELECT SUM(revenue) total_revenue FROM sales;
