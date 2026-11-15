from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from src.forecasting import METHODS, prepare_data, evaluate_method, make_forecast

st.set_page_config(page_title="Forecasting Dashboard", page_icon="📈", layout="wide")
st.title("📈 Forecasting Dashboard")
st.caption("Explore historical performance, compare forecasting methods, and review future estimates.")

DEFAULT_DATA = Path("data/monthly_sales.csv")

@st.cache_data
def load_default():
    return pd.read_csv(DEFAULT_DATA)

with st.sidebar:
    st.header("Dashboard controls")
    uploaded = st.file_uploader("Upload CSV (date, sales)", type=["csv"])
    horizon = st.slider("Forecast horizon (periods)", min_value=1, max_value=24, value=6)
    method = st.selectbox("Forecasting method", METHODS)
    window = st.slider("Moving-average window", min_value=2, max_value=12, value=3)
    st.caption("The default dataset is synthetic monthly sales data.")

try:
    raw = pd.read_csv(uploaded) if uploaded is not None else load_default()
    data = prepare_data(raw)
except Exception as exc:
    st.error(f"Could not load data: {exc}")
    st.stop()

st.subheader("Historical data")
fig_history = go.Figure()
fig_history.add_trace(go.Scatter(
    x=data["date"], y=data["sales"], mode="lines+markers",
    name="Actual sales", line=dict(width=2)
))
fig_history.update_layout(
    xaxis_title="Date", yaxis_title="Sales",
    hovermode="x unified", template="plotly_white",
    margin=dict(l=20, r=20, t=25, b=20)
)
st.plotly_chart(fig_history, use_container_width=True)

try:
    metrics = evaluate_method(data, method, window)
    forecast = make_forecast(data, horizon, method, window)
except Exception as exc:
    st.error(f"Forecast could not be calculated: {exc}")
    st.stop()

latest = float(data["sales"].iloc[-1])
avg_forecast = float(forecast["forecast"].mean())
col1, col2, col3 = st.columns(3)
col1.metric("Latest actual", f"{latest:,.2f}")
col2.metric("Average forecast", f"{avg_forecast:,.2f}", f"{avg_forecast-latest:+,.2f}")
col3.metric("Holdout MAE", f'{metrics["mae"]:,.2f}')

st.subheader(f"{method} forecast")
fig_forecast = go.Figure()
fig_forecast.add_trace(go.Scatter(
    x=data["date"], y=data["sales"], mode="lines+markers",
    name="Historical actual"
))
fig_forecast.add_trace(go.Scatter(
    x=forecast["date"], y=forecast["forecast"], mode="lines+markers",
    name="Forecast", line=dict(dash="dash")
))
fig_forecast.update_layout(
    xaxis_title="Date", yaxis_title="Sales",
    hovermode="x unified", template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=35, b=20)
)
st.plotly_chart(fig_forecast, use_container_width=True)

left, right = st.columns([1, 1])
with left:
    st.subheader("Forecast values")
    st.dataframe(forecast, use_container_width=True, hide_index=True)
    st.download_button(
        "Download forecast CSV",
        data=forecast.to_csv(index=False).encode("utf-8"),
        file_name="forecast.csv",
        mime="text/csv"
    )
with right:
    st.subheader("Holdout evaluation")
    st.write(f"**RMSE:** {metrics['rmse']:,.2f}")
    st.write(f"**MAE:** {metrics['mae']:,.2f}")
    st.write(f"Training observations: {metrics['train_observations']}")
    st.write(f"Test observations: {metrics['test_observations']}")
    st.caption("Metrics use the latest 20% of observations as a chronological holdout. Lower errors indicate better fit on this test period.")
