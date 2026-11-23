"""Dependency-audit helper that invokes pip-audit when installed."""
import shutil
import subprocess
import sys

def main():
    if not shutil.which("pip-audit"):
        print("pip-audit is not installed.")
        print("Install with: python -m pip install pip-audit")
        print("Then run: pip-audit -r requirements.txt")
        return 2
    return subprocess.call(["pip-audit"])

if __name__ == "__main__":
    raise SystemExit(main())
