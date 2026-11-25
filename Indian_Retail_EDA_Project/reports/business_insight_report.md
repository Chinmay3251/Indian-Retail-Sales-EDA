# Indian Retail Sales — Exploratory Data Analysis Report

## Executive summary
This project analyzes a 5,000-row Indian retail/e-commerce-style order dataset using Python, Pandas, NumPy and Matplotlib. **Important: the included dataset is synthetic, generated for learning and reproducible demonstration. It is not actual company or Kaggle data.**

- Orders: 5,000
- Period: 2024-01-01 to 2025-12-31
- Net sales: ₹48,336,697.73
- Estimated profit: ₹13,991,598.65
- Average order value: ₹9,667.34
- Return rate: 4.60%
- Cancellation rate: 2.22%

## Dataset and preparation
Each row represents an order, with date, city, category, product, price, quantity, discount, gross/net sales, estimated cost/profit, payment method, sales channel, customer type and order status. Currency is INR.

Preparation: parsed order dates; checked duplicates and missing values; removed duplicate order IDs; filled missing city/payment labels with `Unknown`; created month and margin features; grouped sales by category, city, channel and month.

### Data-quality checks
- Rows: 5000; columns: 16
- Duplicate order IDs: 0
- Missing cells before cleaning: 35
- Missing city: 17
- Missing payment method: 18

## Five key business findings

### Finding 1
Electronics is the largest sales category, contributing ₹32,780,658 (67.8% of net sales). Protect availability and monitor category-level margin.

### Finding 2
Bengaluru leads city sales at ₹8,930,874 (18.5% of net sales). Review local demand, delivery capacity and customer acquisition before reallocating budget.

### Finding 3
Mobile App is the leading channel at ₹22,901,774 (47.4% of net sales). Compare conversion and profitability across channels, not sales alone.

### Finding 4
2025-01 is the strongest month, with ₹2,538,085 in net sales. Review campaign timing and inventory plans around this peak; validate with real historical data before forecasting.

### Finding 5
Returned orders account for 4.6% and cancelled orders 2.2% of all orders. Track reasons by category, city and channel to identify avoidable revenue leakage.

## Business recommendations
1. Protect stock availability in the top category and monitor its margin.
2. Use city performance to prioritize logistics and localized marketing.
3. Improve the leading channel's customer journey while comparing channel-level profit.
4. Use monthly patterns as a planning input, but validate seasonality using actual business history.
5. Build a returns/cancellations dashboard and investigate reasons before changing policy.

## Limitations
- All data and resulting insights are synthetic demonstration values, not actual Indian market performance.
- Costs and profit are simulated estimates, not audited financial figures.
- No customer identifier is provided, so customer retention and lifetime value cannot be reliably calculated.
- Descriptive patterns do not prove causation.

## Tools
Python, Pandas, NumPy, Matplotlib, CSV and Jupyter Notebook.
