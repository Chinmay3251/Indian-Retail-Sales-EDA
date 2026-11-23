# W12D5 — 3-Minute Capstone: AI Data Analyst Platform

A local demo platform that lets a business user ask sales questions in plain English, runs read-only analytics in DuckDB, and presents results in Streamlit with Plotly charts.

## Features
- 100,000-row synthetic retail CSV
- KPI summary cards
- Natural-language question interface
- DuckDB analytical SQL
- SQL results returned as Pandas DataFrames
- SQL preview, result table, chart, and CSV download
- Optional local Ollama SQL generation
- Basic read-only SQL guard
- Unit tests and demo documentation

## Quick start (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

## Demo questions
- Which region has the highest revenue?
- Show monthly revenue trend
- What are the top selling products?
- Compare sales channels
- Who are the top customers by revenue?

## Project structure
- `app/streamlit_app.py` — Streamlit application
- `src/analytics.py` — DuckDB setup, SQL guard, query function, intent mapping, optional Ollama
- `data/sales_100k.csv` — synthetic dataset
- `tests/test_sql_guard.py` — SQL guard tests
- `docs/` — architecture, process, setup documentation
- `demo/three_minute_demo_script.md` — presentation narration

## Important limitations
The built-in question mapper supports a limited set of demo intents. Ollama mode is optional. The regex-based SQL guard is not a production-grade security boundary. The app has no authentication or multi-tenant isolation and should remain local for this demo. Runtime tests and benchmark results must be generated on the target machine.
