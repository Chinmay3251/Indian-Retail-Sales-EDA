# Indian Retail Sales EDA Project

## Objective
Complete exploratory data analysis of an Indian retail/e-commerce-style dataset using Python, Pandas and Matplotlib, and present five business findings.

> **Dataset transparency:** The included 5,000-row CSV is synthetic, generated for reproducible learning. It is not actual company data or a downloaded Kaggle dataset. Replace it with an authorized Kaggle download if your internship specifically requires public-source data, and adjust column names if needed.

## Structure
- `data/`: raw and cleaned CSV files
- `notebooks/`: notebook location
- `src/run_eda.py`: reproducible analysis script
- `reports/`: business report, KPIs, summary tables and figures
- `tests/`: basic data checks

## Setup — Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run
```powershell
python src/run_eda.py
```

## Five business questions
1. Which category contributes the most net sales?
2. Which city leads in sales?
3. Which channel generates the highest sales?
4. Which month is strongest?
5. What share of orders are returned or cancelled?

See `reports/business_insight_report.md` for quantified findings and recommendations.

## Interpretation notes
`net_sales_inr` is order value after discount, before return/cancellation reversal. Cost and profit are simulated estimates. No customer ID is supplied, so retention/CLV cannot be calculated. Descriptive patterns do not prove causation.

## Git commands
```powershell
git init
git checkout -b feat/indian-retail-eda
git add data src tests requirements.txt
git commit -m "feat: add Indian retail sales EDA workflow"
git add reports README.md notebooks
 git commit -m "docs: add five business insights and EDA report"
git remote add origin <your-repository-url>
git push -u origin feat/indian-retail-eda
```
