"""Streamlit dashboard to compare registered MLflow model versions."""
import os
import pandas as pd
import streamlit as st
import mlflow
from mlflow.tracking import MlflowClient

DEFAULT_URI = os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")

def get_client(uri: str) -> MlflowClient:
    mlflow.set_tracking_uri(uri)
    return MlflowClient(tracking_uri=uri)

def list_models(client):
    # MLflow 2.x exposes search_registered_models; compatible with recent MLflow.
    return client.search_registered_models(order_by=["name ASC"])

def version_rows(client, registered_model):
    rows = []
    for version in registered_model.latest_versions:
        run = None
        try:
            run = client.get_run(version.run_id)
        except Exception:
            pass
        rows.append({
            "version": str(version.version),
            "run_id": version.run_id,
            "status": version.status,
            "created_at": pd.to_datetime(version.creation_timestamp, unit="ms", utc=True),
            "description": version.description or "",
            "source": version.source or "",
            "aliases": ", ".join(sorted(version.aliases or [])),
            "metrics": dict(run.data.metrics) if run else {},
            "params": dict(run.data.params) if run else {},
            "tags": dict(run.data.tags) if run else {},
        })
    return rows

def main():
    st.set_page_config(page_title="MLflow Model Version Dashboard", layout="wide")
    st.title("MLflow Model Version Dashboard")
    st.caption("Compare registered model versions, run metrics, parameters, and metadata.")

    with st.sidebar:
        st.header("Tracking configuration")
        tracking_uri = st.text_input("MLflow Tracking URI", value=DEFAULT_URI)
        st.caption("Use the same tracking URI used when registering your models.")
        if st.button("Refresh dashboard"):
            st.cache_data.clear()

    try:
        client = get_client(tracking_uri.strip())
        models = list_models(client)
    except Exception as exc:
        st.error(f"Could not connect to MLflow tracking/registry: {exc}")
        st.info("Start MLflow with the same backend store and enter its tracking URI.")
        st.code("mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000")
        return

    if not models:
        st.warning("No registered models were found in this MLflow registry.")
        st.write("Register a model first, then refresh this dashboard.")
        return

    model_names = [m.name for m in models]
    selected_name = st.selectbox("Registered model", model_names)
    selected_model = next(m for m in models if m.name == selected_name)
    rows = version_rows(client, selected_model)

    if not rows:
        st.warning("This registered model has no versions yet.")
        return

    st.subheader(f"Model: {selected_name}")
    st.write(selected_model.description or "No model description provided.")
    df = pd.DataFrame(rows).sort_values("version", key=lambda s: s.astype(int), ascending=False)

    display_df = df[["version", "status", "created_at", "run_id", "aliases", "description"]].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    version_options = df["version"].tolist()
    default_versions = version_options[:min(2, len(version_options))]
    chosen_versions = st.multiselect(
        "Select versions to compare",
        options=version_options,
        default=default_versions,
        help="Select two or more versions for a side-by-side comparison."
    )
    if not chosen_versions:
        st.info("Select at least one model version.")
        return

    compare = df[df["version"].isin(chosen_versions)].copy()
    compare = compare.sort_values("version", key=lambda s: s.astype(int))
    st.subheader("Version comparison")

    metric_names = sorted({key for metrics in compare["metrics"] for key in metrics})
    if metric_names:
        metric = st.selectbox("Metric to visualize", metric_names)
        chart_rows = []
        for _, row in compare.iterrows():
            if metric in row["metrics"]:
                chart_rows.append({"Version": f"v{row['version']}", metric: row["metrics"][metric]})
        if chart_rows:
            chart_df = pd.DataFrame(chart_rows).set_index("Version")
            st.bar_chart(chart_df)
        else:
            st.info("The selected versions do not contain this metric.")
    else:
        st.info("No run metrics were found for the selected model versions.")

    table_rows = []
    for _, row in compare.iterrows():
        item = {
            "Version": f"v{row['version']}",
            "Run ID": row["run_id"],
            "Status": row["status"],
            "Aliases": row["aliases"],
        }
        item.update({f"Metric: {k}": v for k, v in row["metrics"].items()})
        item.update({f"Param: {k}": v for k, v in row["params"].items()})
        table_rows.append(item)
    st.dataframe(pd.DataFrame(table_rows).fillna(""), use_container_width=True, hide_index=True)

    st.subheader("Selected version details")
    detail_version = st.selectbox("Inspect version", chosen_versions, key="detail_version")
    detail = next(row for row in rows if row["version"] == detail_version)
    left, right = st.columns(2)
    with left:
        st.markdown("**Parameters**")
        st.json(detail["params"])
        st.markdown("**Tags**")
        st.json(detail["tags"])
    with right:
        st.markdown("**Version metadata**")
        st.json({
            "version": detail["version"],
            "run_id": detail["run_id"],
            "status": detail["status"],
            "created_at": str(detail["created_at"]),
            "aliases": detail["aliases"],
            "source": detail["source"],
            "description": detail["description"],
        })

if __name__ == "__main__":
    main()
