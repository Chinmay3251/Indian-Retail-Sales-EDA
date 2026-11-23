# Process Documentation

## Build process
1. Defined a demo scope around natural-language business questions over a controlled retail sales dataset.
2. Prepared a deterministic synthetic CSV with 100,000 transaction rows.
3. Implemented DuckDB database initialization from CSV.
4. Added a SQL-to-Pandas DataFrame execution function.
5. Added a read-only SQL validation layer restricting queries to the approved `sales` table.
6. Added a deterministic intent router so the app can demo without an LLM service.
7. Added optional local Ollama SQL generation for an LLM-assisted experience.
8. Built a Streamlit UI with KPI cards, question input, SQL display, result table, Plotly chart, and CSV export.
9. Added unit tests for core SQL guard behavior and documented the architecture and demo sequence.

## Verification status
- CSV generation: completed; 100,000 data rows.
- ZIP integrity: verified during packaging.
- Application runtime: not executed in this environment.
- DuckDB/Streamlit installation: must be completed on the user's machine.
- Ollama mode: optional and requires Ollama service/model locally.
- Security tests: included; run with pytest after installing requirements and pytest.

## Known limitations
- Natural-language coverage in built-in mode is intentionally limited to common demo intents.
- LLM-generated SQL is still subject to a basic regex guard; this is not a substitute for a production SQL parser or isolated read-only database role.
- No authentication or multi-user access control is included.
- Dataset is synthetic and must not be represented as company data.
