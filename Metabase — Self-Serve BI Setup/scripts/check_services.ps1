docker compose ps
try { (Invoke-WebRequest -Uri "http://localhost:8088/health" -UseBasicParsing).StatusCode }
catch { Write-Warning "Superset is not ready. Run: docker compose logs -f superset" }
