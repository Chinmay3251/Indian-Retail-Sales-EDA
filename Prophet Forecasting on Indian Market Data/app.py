from pathlib import Path
import streamlit as st, pandas as pd
from src.data import load_csv,download_market_data
from src.forecast import run_forecast
st.set_page_config(page_title="Indian Market Prophet",layout="wide")
st.title("Indian Market Forecasting with Prophet")
st.caption("Educational demo only — not investment advice.")
ticker=st.sidebar.text_input("Yahoo Finance ticker","^NSEI")
years=st.sidebar.slider("History (years)",1,10,5)
horizon=st.sidebar.slider("Forecast horizon (calendar days)",7,365,90)
offline=st.sidebar.checkbox("Use bundled synthetic sample")
if st.sidebar.button("Run forecast"):
    try:
        data=load_csv("data/sample_indian_market.csv") if offline else download_market_data(ticker,years)
        name="Illustrative sample" if offline else ticker
        summary=run_forecast(data,horizon,"outputs",name,"bundled synthetic sample" if offline else "Yahoo Finance")
        st.success(f"Forecast generated: {name}")
        a,b,c=st.columns(3); a.metric("Observations",summary["observations"])
        b.metric("Last date",summary["last_date"]); c.metric("Horizon",f"{horizon} days")
        st.image("outputs/forecast.png",use_container_width=True)
        if summary["metrics"]: st.subheader("Chronological holdout metrics"); st.json(summary["metrics"])
        st.dataframe(pd.read_csv("outputs/forecast.csv").tail(horizon+10),use_container_width=True)
        st.download_button("Download forecast CSV",Path("outputs/forecast.csv").read_bytes(),"forecast.csv")
    except Exception as e: st.error(str(e))
else: st.info("Select an NSE ticker or the bundled sample, then run the forecast.")
