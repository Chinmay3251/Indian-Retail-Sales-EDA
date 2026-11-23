# Technical Appendix

## DuckDB Python helper
The W12D2 helper exposes:

```python
def query_to_dataframe(sql: str, database: str = ":memory:") -> pd.DataFrame:
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("sql must be a non-empty SQL string")
    with duckdb.connect(database=database) as con:
        return con.execute(sql).fetchdf()
```

Example:

```python
from src.duckdb_analytics import query_to_dataframe

df = query_to_dataframe("""
    SELECT region,
           SUM(quantity * unit_price * (1 - discount_pct)) AS net_revenue
    FROM read_csv_auto('data/sales_100k.csv')
    GROUP BY region
    ORDER BY net_revenue DESC
""")
```

## Security scanner behavior
The W12D3 scanner searches eligible text files for pattern matches associated with:
- Possible hard-coded credentials and private key material
- Debug mode enabled
- Potential SQL string construction patterns
- Disabled TLS certificate verification
- Wildcard CORS origin configuration
- Missing basic repository baseline files

Every match needs context review. A pattern match alone does not prove a vulnerability.

## Benchmark interpretation
The benchmark measures the full path for each run: CSV read plus query/aggregation. It reports median elapsed time from five repetitions. Pandas-over-DuckDB speedup is calculated as:

`Pandas median seconds / DuckDB median seconds`

A value greater than 1 means DuckDB was faster in that run; below 1 means Pandas was faster. Compare only results produced on the same machine and under similar system conditions.

## Security handling
Do not place real secrets, customer data, tokens, or private keys in demo files or screenshots. Use synthetic data and redact evidence.
