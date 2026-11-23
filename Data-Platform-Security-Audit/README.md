# W12D3 — Security Audit on Data Platform

## Purpose
A practical, repeatable security-audit starter kit for a data platform. It checks a local project/repository for common security hygiene issues and provides a structured manual review process.

**Important:** This package is a security review aid, not a penetration test, compliance certification, or proof that a platform is secure. No live cloud account, database, server, or production repository was available for inspection during package creation.

## Included
- `src/security_audit.py` — Python static checks for likely secrets, risky file permissions indicators, unsafe SQL string construction patterns, debug settings, and missing security baseline files.
- `src/dependency_audit.py` — checks installed Python packages for known vulnerabilities when the `pip-audit` tool is installed.
- `docs/security_audit_methodology.md` — scope, process, severity model, and evidence limitations.
- `docs/security_audit_report.md` — report template with findings to validate.
- `docs/security_controls_checklist.md` — data platform control checklist.
- `samples/example.env.example` — safe example environment variable names; no real credentials.
- `reports/` — place generated scan output and evidence here.

## Requirements
Python 3.9+ recommended. The static scanner uses only the Python standard library. Dependency scanning requires network access and `pip-audit`.

## Run (Windows PowerShell)
Run commands separately from the project directory.

```powershell
python src/security_audit.py --target .
```

Optional JSON output:
```powershell
python src/security_audit.py --target . --json reports/static_audit.json
```

Dependency audit (requires pip-audit and package-index access):
```powershell
python -m pip install pip-audit
pip-audit
```

To scan a requirements file:
```powershell
pip-audit -r requirements.txt
```

## Review targets
Review repository files, configuration, secrets management, database access, identity and permissions, network exposure, encryption, backups, logging, monitoring, vulnerability management, and incident response. Use the checklist and report template to record evidence.

## Safe use
- Run against a copy or authorized working tree.
- Do not upload real secrets to Git or include them in audit evidence.
- Treat scanner matches as leads requiring human validation; false positives are possible.
- Never run intrusive tests against systems without explicit authorization.
