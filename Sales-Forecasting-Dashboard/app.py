from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px
from src.pipeline import (METHODS, prepare_sales_data, evaluate_models,
                          build_forecast, make_history_figure,
                          make_forecast_figure, save_pipeline_outputs)

st.set_page_config(page_title="Sales Forecasting Dashboard", page_icon="📊", layout="wide")
st.title("📊 Sales Forecasting Dashboard")
st.write("Explore sales history, compare forecasting models, and generate future estimates.")
st.caption("Training project: bundled data is synthetic. Forecasts are estimates, not guarantees.")

@st.cache_data
def load_sample():
    return pd.read_csv("data/monthly_sales.csv")

with st.sidebar:
    st.header("Data and forecast settings")
    upload = st.file_uploader("Upload a CSV with date and sales columns", type=["csv"])
    horizon = st.slider("Forecast horizon (months / periods)", 1, 24, 6)
    window = st.slider("Moving average window", 2, 12, 3)
    method_choice = st.selectbox("Forecast model", ["Best by holdout RMSE"] + METHODS)
    run = st.button("Generate forecast", type="primary")

try:
    raw = pd.read_csv(upload) if upload is not None else load_sample()
    data = prepare_sales_data(raw)
except Exception as exc:
    st.error(f"Unable to load data: {exc}")
    st.stop()

st.subheader("Historical sales")
st.plotly_chart(make_history_figure(data), use_container_width=True)

seasonality = data.assign(month=data.date.dt.month).groupby("month", as_index=False).sales.mean()
season_fig = px.bar(seasonality, x="month", y="sales", title="Average Sales by Month of Year",
                    labels={"month": "Month", "sales": "Average sales"})
st.plotly_chart(season_fig, use_container_width=True)

comparison = evaluate_models(data, window)
valid = comparison.dropna(subset=["rmse"])
if valid.empty:
    st.error("No forecasting model could be evaluated for this dataset.")
    st.stop()
best_method = str(valid.sort_values("rmse").iloc[0].method)
selected_method = best_method if method_choice == "Best by holdout RMSE" else method_choice

st.subheader("Model comparison")
st.dataframe(comparison, use_container_width=True, hide_index=True)
metric_fig = px.bar(valid, x="method", y="rmse", color="method",
                    title="Holdout RMSE by Forecasting Method",
                    labels={"method": "Method", "rmse": "RMSE"})
st.plotly_chart(metric_fig, use_container_width=True)

if run:
    try:
        forecast = build_forecast(data, horizon, selected_method, window)
        summary = save_pipeline_outputs(data, forecast, comparison, selected_method, "outputs")
        latest = float(data.sales.iloc[-1])
        avg = float(forecast.forecast.mean())
        a, b, c = st.columns(3)
        a.metric("Latest actual sales", f"{latest:,.2f}")
        b.metric("Average forecast", f"{avg:,.2f}", f"{avg-latest:+,.2f}")
        best_row = valid.sort_values("rmse").iloc[0]
        c.metric("Best holdout RMSE", f"{best_row.rmse:,.2f}", str(best_row.method))
        st.subheader(f"Forecast — {selected_method}")
        st.plotly_chart(make_forecast_figure(data, forecast, selected_method),
                        use_container_width=True)
        st.subheader("Forecast values")
        st.dataframe(forecast, use_container_width=True, hide_index=True)
        st.download_button("Download forecast CSV",
                           forecast.to_csv(index=False).encode("utf-8"),
                           file_name="sales_forecast.csv", mime="text/csv")
        st.download_button("Download model comparison CSV",
                           comparison.to_csv(index=False).encode("utf-8"),
                           file_name="model_comparison.csv", mime="text/csv")
        st.success(f"Forecast saved. Selected model: {summary['selected_method']}")
    except Exception as exc:
        st.error(f"Forecast failed: {exc}")
else:
    st.info("Choose your settings and click Generate forecast to create the forecast and download results.")
