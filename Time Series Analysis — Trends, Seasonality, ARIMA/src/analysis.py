from pathlib import Path
import argparse, json, warnings
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

ROOT=Path(__file__).resolve().parents[1]
def load_series(path,date_col,value_col,freq):
    df=pd.read_csv(path)
    if date_col not in df or value_col not in df: raise ValueError("Date/value columns missing")
    df[date_col]=pd.to_datetime(df[date_col],errors="coerce")
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    df=df.dropna(subset=[date_col,value_col]).sort_values(date_col)
    s=df.groupby(date_col)[value_col].mean().sort_index().asfreq(freq).interpolate(method="time").dropna()
    if len(s)<12: raise ValueError("At least 12 regular observations are required")
    return s

def analyze(s,order=(1,1,1),period=12,test_size=6):
    if test_size<1 or len(s)<=test_size+5: raise ValueError("Not enough observations for holdout")
    train,test=s.iloc[:-test_size],s.iloc[-test_size:]
    decomp=seasonal_decompose(train,model="additive",period=period,extrapolate_trend="freq") if len(train)>=2*period else None
    adf=adfuller(train,autolag="AIC")
    fit=ARIMA(train,order=order).fit()
    forecast=fit.forecast(steps=len(test))
    report={"observations":len(s),"arima_order":list(order),"seasonal_period":period,
      "adf_statistic":float(adf[0]),"adf_p_value":float(adf[1]),
      "mae":float(mean_absolute_error(test,forecast)),
      "rmse":float(mean_squared_error(test,forecast)**0.5),
      "forecast":[{"date":str(i),"value":float(v)} for i,v in forecast.items()]}
    return report,decomp,train,test,forecast

def run(csv,date_col,value_col,freq,order,period,test_size,experiment):
    s=load_series(csv,date_col,value_col,freq)
    report,decomp,train,test,forecast=analyze(s,order,period,test_size)
    out=ROOT/"artifacts"; out.mkdir(exist_ok=True)
    fig,ax=plt.subplots(); s.plot(ax=ax,title="Observed time series"); fig.tight_layout(); fig.savefig(out/"observed.png"); plt.close(fig)
    if decomp is not None:
        fig=decomp.plot(); fig.set_size_inches(10,7); fig.tight_layout(); fig.savefig(out/"decomposition.png"); plt.close(fig)
    fig,ax=plt.subplots(); train.plot(ax=ax,label="Train"); test.plot(ax=ax,label="Actual"); forecast.plot(ax=ax,label="Forecast"); ax.legend(); fig.tight_layout(); fig.savefig(out/"forecast.png"); plt.close(fig)
    (out/"report.json").write_text(json.dumps(report,indent=2))
    uri=f"sqlite:///{(ROOT/'mlflow.db').as_posix()}"
    mlflow.set_tracking_uri(uri); mlflow.set_experiment(experiment)
    with mlflow.start_run(run_name="ARIMA-time-series-analysis"):
        mlflow.log_params({"dataset":Path(csv).name,"date_column":date_col,"value_column":value_col,"frequency":freq,"arima_order":str(order),"seasonal_period":period,"test_size":test_size})
        mlflow.log_metrics({k:report[k] for k in ["mae","rmse","adf_statistic","adf_p_value"]})
        mlflow.log_artifacts(str(out),artifact_path="time_series_outputs")
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    warnings.filterwarnings("ignore",category=UserWarning)
    p=argparse.ArgumentParser()
    p.add_argument("--csv",default=str(ROOT/"data/monthly_sales.csv")); p.add_argument("--date-col",default="date")
    p.add_argument("--value-col",default="sales"); p.add_argument("--freq",default="MS")
    p.add_argument("--order",default="1,1,1"); p.add_argument("--period",type=int,default=12)
    p.add_argument("--test-size",type=int,default=6); p.add_argument("--experiment",default="W10D1-Time-Series-ARIMA")
    a=p.parse_args(); order=tuple(map(int,a.order.split(",")))
    if len(order)!=3: p.error("--order must be p,d,q")
    run(a.csv,a.date_col,a.value_col,a.freq,order,a.period,a.test_size,a.experiment)
