import argparse, json
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

REQUIRED={"month","category","revenue","profit","orders"}

def load_data(path):
    df=pd.read_csv(path)
    missing=REQUIRED-set(df.columns)
    if missing: raise ValueError(f"Missing required columns: {sorted(missing)}")
    df["month"]=pd.to_datetime(df["month"],errors="coerce")
    for c in ["revenue","profit","orders"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=["month","category","revenue","profit","orders"])
    if df.empty: raise ValueError("No valid data rows.")
    return df.sort_values("month").reset_index(drop=True)

def calculate_kpis(df):
    rev=float(df.revenue.sum()); prof=float(df.profit.sum())
    monthly=df.groupby("month",as_index=False)[["revenue","profit","orders"]].sum()
    cats=df.groupby("category",as_index=False)[["revenue","profit","orders"]].sum()
    mom=None
    if len(monthly)>1 and monthly.iloc[-2].revenue:
        mom=float((monthly.iloc[-1].revenue/monthly.iloc[-2].revenue-1)*100)
    k={"total_revenue":rev,"total_profit":prof,"total_orders":int(df.orders.sum()),
       "profit_margin":prof/rev if rev else 0,
       "latest_month_change_pct":mom,
       "top_category":str(cats.loc[cats.revenue.idxmax(),"category"]),
       "period_start":str(df.month.min().date()),"period_end":str(df.month.max().date())}
    return k,monthly,cats

def make_charts(monthly,cats,out):
    out.mkdir(parents=True,exist_ok=True)
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=monthly.month,y=monthly.revenue,name="Revenue",mode="lines+markers"))
    fig.add_trace(go.Scatter(x=monthly.month,y=monthly.profit,name="Profit",mode="lines+markers",yaxis="y2"))
    fig.update_layout(title="Revenue and Profit Trend",template="plotly_white",
        xaxis_title="Month",yaxis=dict(title="Revenue"),yaxis2=dict(title="Profit",overlaying="y",side="right"))
    fig.write_image(str(out/"monthly_trend.png"),width=1200,height=600,scale=2)
    bar=px.bar(cats.sort_values("revenue",ascending=False),x="category",y="revenue",
               title="Revenue by Category",template="plotly_white")
    bar.write_image(str(out/"category_revenue.png"),width=1200,height=600,scale=2)
    return out/"monthly_trend.png",out/"category_revenue.png"

def textbox(slide,text,x,y,w,h,size=16,bold=False,color=(40,55,75)):
    shape=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    p=shape.text_frame.paragraphs[0]; p.text=text
    p.font.size=Pt(size); p.font.bold=bold; p.font.color.rgb=RGBColor(*color)
    return shape

def title(slide,heading,sub=""):
    textbox(slide,heading,.55,.25,12,.55,25,True)
    if sub: textbox(slide,sub,.6,.85,12,.35,10,False,(100,110,120))

def add_kpi(slide,x,label,value):
    sh=slide.shapes.add_shape(1,Inches(x),Inches(3.0),Inches(2.85),Inches(1.1))
    sh.fill.solid(); sh.fill.fore_color.rgb=RGBColor(237,243,249)
    sh.line.color.rgb=RGBColor(210,220,230)
    tf=sh.text_frame; tf.clear()
    p=tf.paragraphs[0]; p.text=label; p.font.size=Pt(10)
    p2=tf.add_paragraph(); p2.text=value; p2.font.size=Pt(19); p2.font.bold=True

def build_deck(k,trend_img,cat_img,path):
    prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
    blank=prs.slide_layouts[6]
    s=prs.slides.add_slide(blank); title(s,"Executive Sales Performance",f"Reporting period: {k['period_start']} to {k['period_end']} | Synthetic practice data")
    textbox(s,"Executive takeaway",.65,1.35,4,.35,15,True,(30,80,130))
    textbox(s,f"Revenue totaled {k['total_revenue']:,.0f}. {k['top_category']} was the largest category by revenue. Review profitability alongside revenue before deciding where to scale.",.65,1.8,12,.8,16)
    add_kpi(s,.65,"TOTAL REVENUE",f"{k['total_revenue']:,.0f}")
    add_kpi(s,3.85,"TOTAL PROFIT",f"{k['total_profit']:,.0f}")
    add_kpi(s,7.05,"PROFIT MARGIN",f"{k['profit_margin']:.1%}")
    add_kpi(s,10.25,"TOTAL ORDERS",f"{k['total_orders']:,}")
    mom="N/A" if k["latest_month_change_pct"] is None else f"{k['latest_month_change_pct']:+.1f}%"
    textbox(s,f"Latest month revenue change vs previous month: {mom}",.75,4.55,11,.4,14,True)
    textbox(s,"Data note: synthetic practice dataset; values do not represent a real company.",.75,6.7,11,.3,9,False,(110,110,110))
    s=prs.slides.add_slide(blank); title(s,"Revenue and Profit Trend","Compare revenue movement with profit movement over the reporting period.")
    s.shapes.add_picture(str(trend_img),Inches(.7),Inches(1.3),width=Inches(11.9))
    s=prs.slides.add_slide(blank); title(s,"Category Revenue Contribution","Review category scale alongside profitability.")
    s.shapes.add_picture(str(cat_img),Inches(.7),Inches(1.3),width=Inches(11.9))
    textbox(s,f"Top category by revenue: {k['top_category']}. Validate its profit and margin before prioritizing investment.",.8,6.65,11,.4,12)
    s=prs.slides.add_slide(blank); title(s,"Recommendations and Next Steps","Turn the performance review into measurable follow-up.")
    actions=[
      ("1. Review profitability","Compare profit margin by category; flag high-revenue areas with weaker returns."),
      ("2. Investigate drivers","Check pricing, discounts, product mix, and order volume before drawing causal conclusions."),
      ("3. Test a focused action","Run a time-bound improvement test in one selected category or segment."),
      ("4. Track outcomes","Monitor revenue, profit, margin, and orders against a comparable baseline.")]
    y=1.5
    for h,b in actions:
        textbox(s,h,.8,y,3,.4,15,True,(30,80,130)); textbox(s,b,3.6,y,8.7,.55,13); y+=1.15
    textbox(s,"Decision requested: agree on the segment to investigate and success measures for the next review.",.8,6.4,11.5,.5,14,True)
    prs.save(path)

def run(input_path,output):
    out=Path(output); out.mkdir(parents=True,exist_ok=True)
    df=load_data(input_path); k,m,c=calculate_kpis(df)
    ti,ci=make_charts(m,c,out)
    m.to_csv(out/"monthly_kpis.csv",index=False); c.to_csv(out/"category_kpis.csv",index=False)
    (out/"executive_summary.json").write_text(json.dumps(k,indent=2))
    deck=out/"executive_report.pptx"; build_deck(k,ti,ci,deck)
    return k,deck

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",default="data/monthly_business_performance.csv")
    p.add_argument("--output",default="outputs"); a=p.parse_args()
    k,d=run(a.input,a.output); print(json.dumps(k,indent=2)); print("PowerPoint:",d)
if __name__=="__main__": main()
