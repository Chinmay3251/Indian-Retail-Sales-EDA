# Chart Creation Guide (5 Required Charts)

Use the `sample_sales` dataset. If the charts are not yet created, make them via **Charts → + Chart**. Choose the dataset, select the visualization, configure, and save. Add each saved chart to the dashboard named **Sales Overview Dashboard**.

## 1. Bar chart — Revenue by Category
- Visualization: Bar Chart (ECharts)
- X-axis: `category`
- Metric: `SUM(revenue)`
- Sort: revenue descending
- Chart title: Revenue by Category
- Save chart to dashboard.

## 2. Line chart — Monthly Revenue Trend
- Visualization: Line Chart
- Time column: `order_date`
- Time grain: Month
- Metric: `SUM(revenue)`
- Chart title: Monthly Revenue Trend
- Save to dashboard.

## 3. Pie chart — Revenue Share by Category
- Visualization: Pie Chart
- Dimension/group: `category`
- Metric: `SUM(revenue)`
- Chart title: Revenue Share by Category
- Save to dashboard.

## 4. Table — Product Sales Details
- Visualization: Table
- Columns: `product`, `category`, `region`, `quantity`, `revenue`, `profit`
- Sort: revenue descending
- Chart title: Product Sales Details
- Save to dashboard.

## 5. Metric card — Total Revenue
- Visualization: Big Number (or Big Number with Trendline)
- Metric: `SUM(revenue)`
- Chart title: Total Revenue
- Save to dashboard.

## Dashboard layout suggestion
Top row: Total Revenue metric card.
Second row: Revenue by Category (bar) and Revenue Share by Category (pie).
Third row: Monthly Revenue Trend (line).
Bottom row: Product Sales Details (table).

Once charts are saved, open the dashboard, arrange the charts, save, and verify the layout. Add date/category filters if desired.
