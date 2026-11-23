# Presenter Script — 8 to 10 Minutes

## Opening (45 seconds)
“Today I will demonstrate three parts of the data platform work: the production architecture review, local analytical SQL using DuckDB, and a first-pass repository security audit. The demo uses synthetic data and local scripts.”

## Part 1 — Architecture review (2 minutes)
“First, I reviewed the logical workflow and documented a target architecture. The design separates ingestion, data validation, curated storage, feature processing, model workflows, serving, and monitoring. The review highlights the need for reproducibility, data-quality controls, model governance, access control, monitoring, and rollback. This is a design review, not a live infrastructure audit.”

Show the Mermaid diagram and readiness checklist.

## Part 2 — DuckDB analytics (3 minutes)
“Next, I use DuckDB to query a 100,000-row CSV directly. The SQL examples analyze revenue by region, monthly revenue, product performance, channel performance, and customer value.”

Run the query script and show a result. Then show the Python helper that returns SQL query results as a Pandas DataFrame.

## Part 3 — Performance comparison (1 to 2 minutes)
“I prepared an apples-to-apples benchmark for three analytical queries. Both paths include reading the CSV. The benchmark repeats each query five times and reports the median. The exact timings depend on the demo machine, so I will show the measured results generated here.”

Only show benchmark results after running the script.

## Part 4 — Security audit toolkit (2 minutes)
“The security scanner checks repository text files for patterns that may indicate hard-coded credentials, risky SQL construction, debug configuration, disabled TLS verification, and permissive CORS. It is a first-pass tool. Each match must be validated manually, and a clean scan is not proof of security.”

Run the scanner and show the report template and checklist.

## Closing (45 seconds)
“The deliverables are reusable scripts, SQL examples, architecture and security documentation, and a demo runbook. The next steps are to validate findings against the real environment, run and retain benchmark evidence, address prioritized gaps, and obtain platform-owner sign-off.”
