#!/usr/bin/env python3
"""Lightweight repository security hygiene scanner. Standard-library only."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache"}
TEXT_SUFFIXES = {".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
                 ".md", ".sql", ".sh", ".ps1", ".dockerfile", ".txt"}
SECRET_PATTERNS = [
    ("Possible hard-coded credential", re.compile(r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]{6,}['\"]")),
    ("Possible private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Possible cloud access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
]
RISK_PATTERNS = [
    ("Debug mode enabled", re.compile(r"(?i)\b(DEBUG|debug)\s*[:=]\s*(true|1|['\"]true['\"])")),
    ("Potential SQL built with string interpolation/concatenation", re.compile(r"(?i)(execute|executemany)\s*\(\s*(f['\"]|['\"].{0,120}\+\s*[a-zA-Z_])")),
    ("TLS certificate verification disabled", re.compile(r"(?i)(verify\s*=\s*False|CERT_NONE)")),
    ("Wildcard CORS origin", re.compile(r"(?i)(allow_origins|cors_origins)\s*[:=]\s*\[[^\]]*['\"]\*['\"]")),
]
BASELINE_FILES = ["README.md", ".gitignore"]

def scan(target: Path):
    findings = []
    scanned = 0
    for path in target.rglob("*"):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name.lower() not in {"dockerfile", "makefile"}:
            continue
        try:
            if path.stat().st_size > 2_000_000:
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        scanned += 1
        rel = str(path.relative_to(target))
        for label, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append({"severity": "HIGH", "type": label, "file": rel, "line": line,
                                 "evidence": "Matched pattern; inspect locally and do not copy secret values into reports."})
        for label, pattern in RISK_PATTERNS:
            for match in pattern.finditer(content):
                line = content.count("\n", 0, match.start()) + 1
                findings.append({"severity": "MEDIUM", "type": label, "file": rel, "line": line,
                                 "evidence": "Potentially risky configuration/code pattern; validate context."})
    for name in BASELINE_FILES:
        if not (target / name).exists():
            findings.append({"severity": "LOW", "type": f"Missing baseline file: {name}",
                             "file": ".", "line": None,
                             "evidence": "Add project documentation or ignore rules as appropriate."})
    return {"target": str(target.resolve()), "files_scanned": scanned, "finding_count": len(findings),
            "findings": findings,
            "limitations": ["Pattern-based checks can produce false positives and false negatives.",
                            "This tool does not inspect live infrastructure, cloud IAM, network rules, databases, or runtime behavior.",
                            "A clean scan is not proof of security."]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Repository or project directory to scan")
    parser.add_argument("--json", dest="json_path", help="Optional path to save JSON report")
    args = parser.parse_args()
    target = Path(args.target)
    if not target.exists() or not target.is_dir():
        raise SystemExit(f"Target directory does not exist: {target}")
    result = scan(target)
    print(f"Scanned files: {result['files_scanned']}")
    print(f"Findings: {result['finding_count']}")
    for item in result["findings"]:
        print(f"[{item['severity']}] {item['type']} — {item['file']}:{item['line']}")
    if args.json_path:
        out = Path(args.json_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(f"JSON report saved: {out}")
    print("Note: findings require human validation; this is not a complete security audit.")

if __name__ == "__main__":
    main()
