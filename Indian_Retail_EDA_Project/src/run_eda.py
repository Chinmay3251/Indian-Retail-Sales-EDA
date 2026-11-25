from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data/indian_retail_sales.csv"
OUT=ROOT/"reports"; FIG=OUT/"figures"; FIG.mkdir(parents=True,exist_ok=True)
df=pd.read_csv(DATA,parse_dates=["order_date"])
print("Shape:",df.shape,"\\nMissing values:\\n",df.isna().sum())
print("Duplicate order IDs:",df.order_id.duplicated().sum())
df=df.drop_duplicates("order_id").copy()
df["city"]=df.city.fillna("Unknown"); df["payment_method"]=df.payment_method.fillna("Unknown")
df["month"]=df.order_date.dt.to_period("M").astype(str)
df["margin_pct"]=np.where(df.net_sales_inr.ne(0),df.estimated_profit_inr/df.net_sales_inr*100,0)
df.to_csv(ROOT/"data/cleaned_indian_retail_sales.csv",index=False)
kpis={"orders":len(df),"net_sales_inr":df.net_sales_inr.sum(),"estimated_profit_inr":df.estimated_profit_inr.sum(),"average_order_value_inr":df.net_sales_inr.mean(),"return_rate_pct":df.order_status.eq("Returned").mean()*100,"cancellation_rate_pct":df.order_status.eq("Cancelled").mean()*100}
pd.Series(kpis,name="value").to_csv(OUT/"kpi_summary.csv")
df.describe(include="all").to_csv(OUT/"descriptive_statistics.csv")
for col,file in [("category","category_sales.csv"),("city","city_sales.csv"),("sales_channel","channel_sales.csv"),("month","monthly_sales.csv")]: df.groupby(col).net_sales_inr.sum().sort_values(ascending=False).to_csv(OUT/file)
def plot(s,title,ylabel,file,h=False):
 fig,ax=plt.subplots(figsize=(10,5.5)); (s.sort_values() if h else s/100000).plot(kind="barh" if h else "bar",ax=ax); ax.set_title(title); ax.set_ylabel(ylabel); ax.set_xlabel(""); ax.grid(axis="x" if h else "y",alpha=.25); fig.tight_layout(); fig.savefig(FIG/file,dpi=150); plt.close(fig)
plot(df.groupby("category").net_sales_inr.sum(),"Net Sales by Product Category","Net sales (₹ lakh)","sales_by_category.png")
plot(df.groupby("city").net_sales_inr.sum(),"Net Sales by City","Net sales (₹)","sales_by_city.png",True)
plot(df.groupby("sales_channel").net_sales_inr.sum(),"Net Sales by Sales Channel","Net sales (₹ lakh)","sales_by_channel.png")
monthly=df.groupby("month").net_sales_inr.sum().sort_index(); fig,ax=plt.subplots(figsize=(11,5)); monthly.plot(ax=ax,marker="o"); ax.set_title("Monthly Net Sales Trend"); ax.set_ylabel("Net sales (₹)"); ax.tick_params(axis="x",rotation=60); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(FIG/"monthly_sales_trend.png",dpi=150); plt.close(fig)
print("Analysis outputs saved to",OUT)
