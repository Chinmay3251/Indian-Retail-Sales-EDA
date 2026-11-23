# Demo Runbook — W12D4

## Before the demo
- Extract the W12D2 and W12D3 project ZIPs.
- Open each project folder in VS Code.
- Use synthetic/demo data only.
- Confirm Python is installed.
- Install dependencies where package-index access is available.
- Run each command before the presentation and save the actual outputs.
- Do not claim the architecture review is a live audit or that unrun tests passed.

## Demo 1 — DuckDB SQL analytics
From the W12D2 project directory, run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/run_queries.py
```

Show the five analytical query outputs.

## Demo 2 — SQL to Pandas DataFrame
Run a short Python example:

```powershell
python -c "from src.duckdb_analytics import query_to_dataframe; print(query_to_dataframe("SELECT region, COUNT(*) AS orders FROM read_csv_auto('data/sales_100k.csv') GROUP BY region ORDER BY orders DESC"))"
```

If shell quoting is inconvenient, use a small temporary Python file with the example from `docs/technical_appendix.md`.

## Demo 3 — DuckDB vs Pandas benchmark
Run:

```powershell
python src/benchmark.py
```

Show `reports/benchmark_results.csv`. Explain that the script uses five repetitions and median timings, and that results are machine-dependent.

## Demo 4 — Security audit toolkit
From the W12D3 project directory, run:

```powershell
python src/security_audit.py --target .
```

Optionally save a JSON report:

```powershell
python src/security_audit.py --target . --json reports/static_audit.json
```

Explain that matches are candidate findings and require manual validation.

## Demo 5 — Architecture and readiness
Open:
- `docs/production_architecture_review.md`
- `architecture/target_architecture.mmd`
- `checklists/production_readiness_checklist.md`

Explain the highest-priority gaps: data quality, reproducibility, model validation, secrets/access control, monitoring, and rollback.

## Troubleshooting
- If `duckdb` import fails, verify the virtual environment is active and install `requirements.txt`.
- If installation fails, check network/package-index access and retry on an approved network.
- If PowerShell quoting fails, put SQL in a `.py` file rather than nesting quotes in `python -c`.
- If security scanner findings appear, inspect the referenced file and line; do not copy secret values into slides or reports.
- If no findings appear, do not claim the platform is secure; the scanner has limited scope.

## Demo close
Summarize what was demonstrated, list any steps that could not be run, show generated evidence, and state the next actions with owners.
