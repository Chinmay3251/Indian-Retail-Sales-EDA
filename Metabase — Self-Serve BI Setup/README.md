# W11D4 — Apache Superset BI Dashboard

## Included
Docker Compose setup for Apache Superset + PostgreSQL, automatic sample sales table initialization, SQL queries for all five charts, service check script, and guides for dashboard creation, PNG export, and stakeholder sharing.

## Prerequisites
Docker Desktop and Windows PowerShell.

## Start locally
```powershell
docker compose up -d
docker compose ps
```
Open http://localhost:8088 after initialization. Local demo login: `admin` / `admin`. These credentials and the included secret key are for local practice only.

## Connect PostgreSQL in Superset
Settings → Database Connections → + Database.
SQLAlchemy URI:
`postgresql+psycopg2://analyst:analyst_local_password@warehouse-db:5432/analytics`
Use `warehouse-db` as host because Superset runs inside Docker. Test and save.

## Dataset
Data → Datasets → + Dataset → database connection → schema `public` → table `sales`.

## Dashboard
Follow `docs/dashboard-build.md` to create all five charts. SQL equivalents are in `sql/chart_queries.sql`.
Follow `docs/png-export.md` and `docs/stakeholder-sharing.md`.

## Stop
```powershell
docker compose down
```
To delete the demo data volume too:
```powershell
docker compose down -v
```

## Git (replace [name])
```powershell
git checkout -b feat/w11d4-[name]
git add .
git commit -m "feat: superset bi dashboard setup and charts"
git add README.md docs sql
git commit -m "docs: add chart queries, PNG export and stakeholder sharing"
git push -u origin feat/w11d4-[name]
git log -2 --oneline
git status
```
Security: replace demo credentials and secret key, and configure proper authentication/TLS before sharing beyond your local machine.
