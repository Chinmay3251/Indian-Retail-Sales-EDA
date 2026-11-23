import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import plotly.express as px
from src.analytics import initialize_database, run_sql, kpi_summary, suggested_sql, generate_sql_with_ollama, DB_PATH

st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")
st.title("📊 AI Data Analyst Platform")
st.caption("Ask business questions in plain English. DuckDB runs the analytics locally.")

if "db_ready" not in st.session_state:
    with st.spinner("Preparing the demo analytics database..."):
        initialize_database()
    st.session_state.db_ready = True

with st.sidebar:
    st.header("Platform settings")
    use_ollama = st.toggle("Use local Ollama LLM (optional)", value=False)
    model = st.text_input("Ollama model", value="qwen2.5:1.5b", disabled=not use_ollama)
    st.markdown("---")
    st.write("**Data source:** Synthetic retail sales CSV")
    st.write("**Query engine:** DuckDB")
    st.write("**Result format:** Pandas DataFrame")

kpis = kpi_summary()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Orders", f"{int(kpis['orders']):,}")
c2.metric("Customers", f"{int(kpis['customers']):,}")
c3.metric("Net revenue", f"₹{kpis['net_revenue']:,.2f}")
c4.metric("Average order value", f"₹{kpis['avg_order_value']:,.2f}")

st.subheader("Ask your data")
examples = [
    "Which region has the highest revenue?",
    "Show monthly revenue trend",
    "What are the top selling products?",
    "Compare sales channels",
    "Who are the top customers by revenue?"
]
chosen = st.selectbox("Try an example question", ["Choose a question..."] + examples)
question = st.text_input("Your question", value="" if chosen == "Choose a question..." else chosen,
                         placeholder="e.g. Which region has the highest revenue?")
if st.button("Analyze", type="primary", disabled=not question.strip()):
    sql = generate_sql_with_ollama(question, model=model) if use_ollama else None
    mode = "Ollama-generated SQL" if sql else "Built-in safe question mapping"
    if not sql:
        sql = suggested_sql(question)
    try:
        result = run_sql(sql)
        st.success(f"Analysis completed using {mode}.")
        st.markdown("**Generated SQL**")
        st.code(sql, language="sql")
        st.markdown("**Query result**")
        st.dataframe(result, use_container_width=True)
        numeric = [c for c in result.columns if c not in ["region","product","channel","category","customer_id","month"]]
        dims = [c for c in result.columns if c not in numeric]
        if dims and numeric and len(result) > 0:
            fig = px.bar(result, x=dims[0], y=numeric[-1], title=f"{numeric[-1]} by {dims[0]}")
            st.plotly_chart(fig, use_container_width=True)
        st.download_button("Download results as CSV", result.to_csv(index=False), "analysis_results.csv", "text/csv")
    except Exception as e:
        st.error(f"Could not run analysis: {e}")

st.markdown("---")
st.subheader("Platform capabilities")
a,b,c = st.columns(3)
a.info("**Natural-language interface**\\n\\nAsk questions in plain English.")
b.info("**SQL analytics**\\n\\nDuckDB executes read-only analytical SQL.")
c.info("**Visual reporting**\\n\\nTables, charts, and CSV export.")
st.caption("Demo note: dataset is synthetic. LLM mode requires a locally running Ollama server and a pulled model. Built-in mode works without Ollama.")
