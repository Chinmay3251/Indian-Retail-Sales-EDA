"""DuckDB-backed analytics and guarded SQL execution."""
from pathlib import Path
import re
import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV = ROOT / "data" / "sales_100k.csv"
DB_PATH = ROOT / "data" / "analytics.duckdb"

def initialize_database(csv_path=DEFAULT_CSV, db_path=DB_PATH):
    csv_path = Path(csv_path).resolve()
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    safe_path = str(csv_path).replace("'", "''")
    con.execute(f"""
        CREATE OR REPLACE TABLE sales AS
        SELECT * FROM read_csv_auto('{safe_path}', header=true)
    """)
    con.close()

def validate_readonly_sql(sql: str) -> str:
    """Allow a single read-only SELECT/WITH statement against the sales table."""
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("Please provide a SQL query.")
    cleaned = sql.strip()
    # Remove trailing semicolon(s), reject multiple statements.
    if ";" in cleaned.rstrip(";"):
        raise ValueError("Only one SQL statement is allowed.")
    cleaned = cleaned.rstrip(";").strip()
    if not re.match(r"(?is)^(SELECT|WITH)\b", cleaned):
        raise ValueError("Only read-only SELECT or WITH queries are allowed.")
    forbidden = re.compile(r"(?i)\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|COPY|ATTACH|DETACH|INSTALL|LOAD|EXPORT|IMPORT|PRAGMA|CALL|SET|RESET)\b")
    if forbidden.search(cleaned):
        raise ValueError("Query contains a restricted SQL operation.")
    if re.search(r"(?i)\b(read_csv|read_parquet|read_json|glob|sqlite_scan|postgres_scan)\s*\(", cleaned):
        raise ValueError("External file and database table functions are disabled in demo SQL.")
    if not re.search(r"(?i)\bFROM\s+sales\b", cleaned):
        raise ValueError("Queries must read from the approved sales table.")
    return cleaned

def run_sql(sql: str, db_path=DB_PATH) -> pd.DataFrame:
    safe_sql = validate_readonly_sql(sql)
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        return con.execute(safe_sql).fetchdf()
    finally:
        con.close()

def kpi_summary(db_path=DB_PATH):
    q = """
    SELECT COUNT(*) AS orders,
           COUNT(DISTINCT customer_id) AS customers,
           ROUND(SUM(quantity * unit_price * (1-discount_pct)),2) AS net_revenue,
           ROUND(AVG(quantity * unit_price * (1-discount_pct)),2) AS avg_order_value,
           ROUND(100.0 * SUM(CASE WHEN discount_pct > 0 THEN 1 ELSE 0 END) / COUNT(*),2) AS discounted_order_pct
    FROM sales
    """
    con = duckdb.connect(str(db_path), read_only=True)
    try:
        return con.execute(q).fetchdf().iloc[0].to_dict()
    finally:
        con.close()

def suggested_sql(question: str) -> str:
    """Small deterministic intent router used when Ollama is unavailable."""
    q = question.lower()
    if any(x in q for x in ["region", "regional"]):
        return """SELECT region, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) AS revenue
                  FROM sales GROUP BY region ORDER BY revenue DESC"""
    if any(x in q for x in ["month", "monthly", "trend", "over time"]):
        return """SELECT DATE_TRUNC('month', CAST(order_date AS DATE)) AS month,
                  ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) AS revenue
                  FROM sales GROUP BY month ORDER BY month"""
    if any(x in q for x in ["product", "top selling", "best selling"]):
        return """SELECT product, SUM(quantity) AS units,
                  ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) AS revenue
                  FROM sales GROUP BY product ORDER BY revenue DESC LIMIT 10"""
    if any(x in q for x in ["channel"]):
        return """SELECT channel, COUNT(*) AS orders,
                  ROUND(AVG(quantity*unit_price*(1-discount_pct)),2) AS avg_order_value
                  FROM sales GROUP BY channel ORDER BY avg_order_value DESC"""
    if any(x in q for x in ["customer", "customers"]):
        return """SELECT customer_id, COUNT(*) AS orders,
                  ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) AS revenue
                  FROM sales GROUP BY customer_id ORDER BY revenue DESC LIMIT 10"""
    return """SELECT category, ROUND(SUM(quantity*unit_price*(1-discount_pct)),2) AS revenue
              FROM sales GROUP BY category ORDER BY revenue DESC"""

def generate_sql_with_ollama(question: str, model="qwen2.5:1.5b", host="http://localhost:11434"):
    """Optional local LLM SQL generation. Returns None if Ollama is unavailable."""
    import requests
    prompt = f"""You are a SQL analyst. Table: sales(order_id, order_date, customer_id, product,
category, region, channel, quantity, unit_price, discount_pct).
Generate exactly one read-only DuckDB SELECT query using only table sales.
Do not use external file functions, DDL, DML, PRAGMA, or multiple statements.
Return SQL only. User question: {question}"""
    try:
        response = requests.post(
            f"{host.rstrip('/')}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=25
        )
        response.raise_for_status()
        raw = response.json().get("response", "").strip()
        raw = raw.replace("```sql", "").replace("```", "").strip()
        return validate_readonly_sql(raw)
    except Exception:
        return None
