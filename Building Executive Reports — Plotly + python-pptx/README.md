# W11D2 — Executive Reports with Plotly + python-pptx

Build an executive-ready PowerPoint from monthly business data. Plotly creates charts and python-pptx assembles slides. Bundled data is synthetic and for practice only.

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
## Generate the report
```powershell
python -m src.build_report
```
Output: `outputs/executive_report.pptx`, charts, CSV summaries, and JSON KPI summary.

Use another CSV:
```powershell
python -m src.build_report --input data/monthly_business_performance.csv --output outputs
```
Required CSV columns: `month`, `category`, `revenue`, `profit`, `orders`.

## Report structure
1. Executive summary and KPI scorecard
2. Revenue and profit trend
3. Category revenue contribution
4. Recommendations and next steps

## Tests
```powershell
pytest -q
```

## Git workflow
```powershell
git checkout -b feat/w11d2-executive-reports
git add .
git commit -m "feat: generate executive PowerPoint reports with Plotly charts"
git add README.md docs tests
git commit -m "test: add report data checks and document executive workflow"
git push -u origin feat/w11d2-executive-reports
git log -2 --oneline
git status
```
If branch exists, use `git checkout feat/w11d2-executive-reports`. Verify `origin` with `git remote -v` before pushing.
