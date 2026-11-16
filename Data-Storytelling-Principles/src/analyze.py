import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED = {"order_id","order_date","category","region","sales","profit","quantity","discount"}

def load_data(path):
    df = pd.read_csv(path)
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    for c in ["sales","profit","quantity","discount"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["order_date","sales","profit","quantity","discount"])
    if df.empty:
        raise ValueError("No valid records found.")
    return df

def analyze(df, output):
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    category=df.groupby("category",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"),orders=("order_id","nunique"))
    category["profit_margin"]=category["profit"]/category["sales"].replace(0,pd.NA)
    region=df.groupby("region",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"),orders=("order_id","nunique"))
    region["profit_margin"]=region["profit"]/region["sales"].replace(0,pd.NA)
    monthly=df.assign(month=df.order_date.dt.to_period("M").dt.to_timestamp()).groupby("month",as_index=False).agg(sales=("sales","sum"),profit=("profit","sum"))
    category.to_csv(out/"category_summary.csv",index=False)
    region.to_csv(out/"region_summary.csv",index=False)
    monthly.to_csv(out/"monthly_summary.csv",index=False)
    for frame,x,y,title,file,kind in [
        (category,"category","sales","Sales by Product Category","sales_by_category.png","bar"),
        (monthly,"month","sales","Monthly Sales Trend","monthly_sales_trend.png","line")]:
        fig,ax=plt.subplots(figsize=(9,5))
        if kind=="bar": ax.bar(frame[x],frame[y])
        else: ax.plot(frame[x],frame[y],marker="o")
        ax.set_title(title); ax.set_xlabel(x.title()); ax.set_ylabel(y.title())
        fig.autofmt_xdate(); fig.tight_layout(); fig.savefig(out/file,dpi=150); plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,5))
    ax.scatter(df.discount,df.profit,alpha=.45)
    ax.set_title("Discount vs Profit — Descriptive Relationship")
    ax.set_xlabel("Discount"); ax.set_ylabel("Profit")
    fig.tight_layout(); fig.savefig(out/"discount_vs_profit.png",dpi=150); plt.close(fig)
    return {"rows":len(df),"total_sales":float(df.sales.sum()),"total_profit":float(df.profit.sum()),
            "top_category":str(category.loc[category.sales.idxmax(),"category"]),
            "top_region":str(region.loc[region.sales.idxmax(),"region"])}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/retail_sales.csv")
    p.add_argument("--output",default="outputs")
    a=p.parse_args()
    result=analyze(load_data(a.input),a.output)
    print(pd.Series(result).to_string())

if __name__=="__main__": main()
