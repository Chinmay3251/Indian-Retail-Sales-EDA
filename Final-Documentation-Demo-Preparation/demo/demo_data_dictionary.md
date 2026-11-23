# Demo CSV Data Dictionary

Dataset: `data/sales_100k.csv` from the W12D2 package. It contains 100,000 synthetic retail transaction rows.

| Column | Meaning | Example / type |
|---|---|---|
| order_id | Unique synthetic order identifier | Integer |
| order_date | Transaction date | YYYY-MM-DD |
| customer_id | Synthetic customer identifier | Integer |
| product | Product name | Text |
| category | Product category | Text |
| region | Sales region | North / South / East / West / Central |
| channel | Sales channel | Online / Store / Partner |
| quantity | Units in the order | Integer |
| unit_price | Unit price | Numeric |
| discount_pct | Discount fraction | 0 to 0.20 |

Net revenue used by the SQL examples is `quantity * unit_price * (1 - discount_pct)`. The dataset is synthetic and should not be represented as real customer or company sales data.
