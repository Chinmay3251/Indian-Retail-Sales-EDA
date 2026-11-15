import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
from src.data import load_csv, download_market_data

def make_model():
    return Prophet(yearly_seasonality=True,weekly_seasonality=True,daily_seasonality=False,
                   seasonality_mode="additive",interval_width=0.95)

def metrics(actual,predicted):
    e=np.asarray(actual)-np.asarray(predicted)
    return {"mae":float(np.mean(np.abs(e))),"rmse":float(np.sqrt(np.mean(e**2)))}

def evaluate_holdout(data):
    split=int(len(data)*0.8)
    if split<30 or len(data)-split<5: return None
    train,test=data.iloc[:split],data.iloc[split:]
    model=make_model(); model.fit(train)
    pred=model.predict(test[["ds"]])
    scored=test.merge(pred[["ds","yhat"]],on="ds")
    result=metrics(scored.y,scored.yhat)
    result.update(train_rows=len(train),test_rows=len(scored))
    return result

def run_forecast(data,period,output_dir,ticker="sample",source="csv"):
    if period<1: raise ValueError("period must be at least one day")
    out=Path(output_dir); out.mkdir(parents=True,exist_ok=True)
    score=evaluate_holdout(data)
    model=make_model(); model.fit(data)
    future=model.make_future_dataframe(periods=period,freq="D")
    forecast=model.predict(future)
    forecast.to_csv(out/"forecast.csv",index=False)
    fig=model.plot(forecast); ax=fig.gca()
    ax.set_title(f"Prophet forecast — {ticker}"); ax.set_xlabel("Date"); ax.set_ylabel("Price")
    fig.tight_layout(); fig.savefig(out/"forecast.png",dpi=150); plt.close(fig)
    summary={"ticker":ticker,"source":source,"observations":len(data),
             "first_date":str(data.ds.min().date()),"last_date":str(data.ds.max().date()),
             "forecast_calendar_days":period,"metrics":score,
             "note":"Experimental estimate, not investment advice; calendar days include non-trading days."}
    (out/"model_summary.json").write_text(json.dumps(summary,indent=2))
    if score: (out/"metrics.json").write_text(json.dumps(score,indent=2))
    return summary

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--ticker",default="^NSEI"); p.add_argument("--years",type=int,default=5)
    p.add_argument("--period",type=int,default=90); p.add_argument("--input")
    p.add_argument("--output",default="outputs"); a=p.parse_args()
    if a.input:
        data=load_csv(a.input); ticker=Path(a.input).stem; source=f"CSV: {a.input}"
    else:
        data=download_market_data(a.ticker,a.years); ticker=a.ticker; source="Yahoo Finance / yfinance"
    print(json.dumps(run_forecast(data,a.period,a.output,ticker,source),indent=2))

if __name__=="__main__": main()
