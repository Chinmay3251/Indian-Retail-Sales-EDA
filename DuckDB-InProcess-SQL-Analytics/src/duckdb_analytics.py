"""DuckDB helper functions."""
from pathlib import Path
import duckdb
import pandas as pd

def query_to_dataframe(sql: str, database: str = ":memory:") -> pd.DataFrame:
    """Execute SQL in DuckDB and return a Pandas DataFrame."""
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("sql must be a non-empty string")
    with duckdb.connect(database=database) as con:
        return con.execute(sql).fetchdf()

def load_csv(csv_path: str, table_name: str = "sales") -> None:
    """Load CSV into a persistent DuckDB table."""
    if not table_name.replace("_", "").isalnum():
        raise ValueError("table_name must be a simple identifier")
    path = str(Path(csv_path).resolve()).replace("\\", "/").replace("'", "''")
    with duckdb.connect("sales.duckdb") as con:
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_csv_auto('{path}')")
