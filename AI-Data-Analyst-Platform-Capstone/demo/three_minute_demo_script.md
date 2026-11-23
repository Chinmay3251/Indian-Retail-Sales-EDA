# Three-Minute Capstone Demo Script

## 0:00–0:25 — Introduction
“This is my AI Data Analyst Platform. It helps business users explore sales data by asking questions in natural language instead of writing SQL manually. The demo uses a synthetic dataset with 100,000 sales transactions.”

## 0:25–0:55 — Platform overview
“Here are the key metrics: order count, unique customers, net revenue, and average order value. DuckDB is the in-process analytics engine, and Streamlit provides the user interface.”

## 0:55–1:45 — Ask a business question
“I’ll ask: Which region has the highest revenue? The platform maps the question to a read-only SQL query, executes it in DuckDB, and returns a Pandas DataFrame. We can inspect the SQL and the results, and the chart makes the comparison easier to understand.”

Then try: “Show monthly revenue trend.”

## 1:45–2:25 — AI and safety
“The platform can optionally use a local Ollama model to generate SQL. If Ollama is unavailable, the built-in question mapping still supports the demo. The SQL guard rejects write operations and queries outside the approved sales table. This is a demo safeguard, not a complete production security system.”

## 2:25–3:00 — Results and close
“Users can view the result table, chart, and download the output as CSV. The next production steps would be stronger SQL parsing, role-based access, audit logging, query limits, monitoring, and deployment hardening.”
