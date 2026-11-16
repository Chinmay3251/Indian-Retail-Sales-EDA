# W11D1 — Data Storytelling: Structure + Narrative

Practical project showing how to turn retail data into a focused business story. The bundled dataset is synthetic and findings are illustrative only.

## Contents
- `data/retail_sales.csv`: synthetic transaction data
- `src/analyze.py`: reusable analysis and chart generation
- `docs/storytelling_framework.md`: story structure and narrative principles
- `docs/example_story.md`: example business narrative and action plan
- `tests/`: basic data validation tests
- `outputs/`: generated summaries and charts

## Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
## Run
```powershell
python -m src.analyze
pytest -q
```

## Workflow
1. Identify the audience and decision.
2. Ask one focused business question.
3. Establish context with relevant KPIs.
4. Select evidence that answers the question.
5. Explain the insight and its business implication.
6. Recommend a practical next action.
7. Define how success will be measured.

## Git
```powershell
git checkout -b feat/w11d1-data-storytelling
git add .
git commit -m "feat: add retail data storytelling analysis and narrative"
git add README.md docs tests
git commit -m "docs: add storytelling framework and example business narrative"
git push -u origin feat/w11d1-data-storytelling
git log -2 --oneline
git status
```
If branch exists, use `git checkout feat/w11d1-data-storytelling`. Check `git remote -v` before push.
