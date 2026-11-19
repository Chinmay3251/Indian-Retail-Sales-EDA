# Create the five-chart dashboard

Use the `sales` dataset and create a dashboard named **Sales Performance Dashboard**. For each chart choose the visualization, configure the fields, save the chart, and add it to the dashboard.

1. **Bar chart — Revenue by Category:** dimension `category`; metric `SUM(revenue)`.
2. **Line chart — Monthly Revenue Trend:** time column `order_date`; time grain Month; metric `SUM(revenue)`.
3. **Pie chart — Revenue Share by Category:** dimension `category`; metric `SUM(revenue)`.
4. **Table — Product Sales Details:** columns `product`, `category`, `region`, `quantity`, `revenue`, `profit`; sort by revenue descending.
5. **Metric card — Total Revenue:** Big Number visualization; metric `SUM(revenue)`.

Layout suggestion: metric card at top; bar and pie in second row; line chart below; table at bottom. Save and verify all five charts load. SQL equivalents are in `sql/chart_queries.sql`.
