from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(label, command):
    print(f"--- {label} ---")
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        print(f"FAILED: {label}")
        raise SystemExit(result.returncode)


run("COMPATIBILITY", [sys.executable, "-m", "pytest", "test/foundation/test_run_compat.py", "-q"])
run("PUBLIC WRAPPERS", [sys.executable, "-m", "pytest", "test/regression/test_public_wrappers.py", "-q"])
run("IMPORT AUDIT", [sys.executable, "-m", "pytest", "test/regression/test_imports_audit.py", "-q"])
run("FULL TEST SUITE", [sys.executable, "-m", "pytest", "-q"])
run("DIFF CHECK", ["git", "diff", "--check"])

print("--- FINAL STATUS ---")
subprocess.run(["git", "status", "--short"], cwd=ROOT, check=True)

print("=== RELEASE VERIFICATION PASS ===")
print("All automated checks passed.")
print("Next steps: git add -> git commit -> git push")
