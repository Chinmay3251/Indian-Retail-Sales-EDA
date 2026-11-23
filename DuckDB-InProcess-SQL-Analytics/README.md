# W12D2 — DuckDB In-Process SQL Analytics

## Included
- 100,000-row synthetic retail CSV: `data/sales_100k.csv`.
- Five analytical SQL queries: `sql/analytical_queries.sql`.
- SQL-to-Pandas helper: `query_to_dataframe(sql)` in `src/duckdb_analytics.py`.
- Three-query DuckDB vs Pandas benchmark: `src/benchmark.py`.
- Query runner: `src/run_queries.py`.

## Windows PowerShell setup (run one command per line)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import duckdb; print(duckdb.__version__)"
```
Run queries: `python src/run_queries.py`
Run benchmark: `python src/benchmark.py`

## Helper example
```python
from src.duckdb_analytics import query_to_dataframe
result = query_to_dataframe("SELECT region, SUM(quantity*unit_price) revenue FROM read_csv_auto('data/sales_100k.csv') GROUP BY region")
print(result.head())
```

The dataset is deterministic synthetic retail data. DuckDB installation could not be completed in the build environment due to unavailable package-index network access. Benchmark timings are therefore not invented; run the benchmark locally to create `reports/benchmark_results.csv`.
