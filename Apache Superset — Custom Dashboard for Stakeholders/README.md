# W11D3 - Apache Superset BI Dashboard (Complete Local Project)

## Deliverables included
- Docker Compose: Superset + PostgreSQL warehouse
- Automatic PostgreSQL sample data initialization
- Local Superset config
- Sample sales data table
- Step-by-step dataset/database setup
- Five-chart dashboard build guide
- PNG export instructions and stakeholder sharing guide
- Git branch and 2-commit workflow

> Local training environment only. Demo credentials and demo passwords must be changed before any non-local use.

## Prerequisites
Install Docker Desktop and ensure Docker Compose is available in PowerShell.

## Start the project
From this folder:
```powershell
docker compose up -d
```
Wait for the Superset container to initialize (first start can take several minutes). Visit:
http://localhost:8088

Login:
- Username: `admin`
- Password: `admin`

**Training-only login.** Change/remove demo credentials for any shared or non-local environment.

## Database connection inside Superset
Go to **Settings → Database Connections → + Database** and connect to the PostgreSQL warehouse:

- Database type: PostgreSQL
- Host: `warehouse-db` (Docker service name; do not use localhost from inside Superset)
- Port: `5432`
- Database: `analytics`
- Username: `analyst`
- Password: `analyst_local_password`

SQLAlchemy URI:
`postgresql+psycopg2://analyst:analyst_local_password@warehouse-db:5432/analytics`

Test connection and save.

## Add dataset
1. Go to **Data → Datasets → + Dataset**.
2. Select database `Sample Sales Warehouse`.
3. Schema: `public`.
4. Table: `sample_sales`.
5. Save.

## Build all five charts
See `docs/chart-build-guide.md` for exact chart configuration.

## Export PNG
See `docs/png-export.md`. Superset dashboard screenshot/export features depend on version and screenshot dependencies; use the documented browser screenshot fallback if native PNG is unavailable.

## Stakeholder sharing
See `docs/stakeholder-sharing.md`.

## Stop and reset
Stop services (data persists):
```powershell
docker compose down
```
Reset demo database volume (WARNING: deletes the sample warehouse data):
```powershell
docker compose down -v
```

## Troubleshooting
- Check status: `docker compose ps`
- View Superset logs: `docker compose logs -f superset`
- Warehouse logs: `docker compose logs -f warehouse-db`
- If the first startup takes time, wait and refresh.
- If ports 8088 or 5433 are occupied, change the host-side port mappings.

## Git tasks (PowerShell commands one per line)
Replace `[name]` with your Git username/name.
```powershell
git checkout -b feat/w11d3-[name]
git add .
git commit -m "feat: superset bi dashboard setup and charts"
git add README.md docs
git commit -m "docs: document dashboard export and stakeholder sharing"
git push -u origin feat/w11d3-[name]
git log -2 --oneline
git status
```
