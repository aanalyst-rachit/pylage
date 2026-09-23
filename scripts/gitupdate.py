from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def run(command: list[str], label: str) -> None:
    print(f"===== {label} =====")
    result = subprocess.run(command, cwd=REPO_ROOT)
    if result.returncode != 0:
        print(f"STOP: {label} failed.")
        sys.exit(result.returncode)


def main() -> None:
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print('Usage: python scripts/gitupdate.py "commit message"')
        sys.exit(2)

    commit_message = " ".join(sys.argv[1:]).strip()

    run(["git", "rev-parse", "--show-toplevel"], "REPOSITORY")
    run(["git", "diff", "--check"], "WORKTREE DIFF CHECK")

    print("===== CURRENT CHANGES =====")
    result = subprocess.run(["git", "status", "--short"], cwd=REPO_ROOT)
    if result.returncode != 0:
        print("STOP: status failed.")
        sys.exit(result.returncode)

    print("===== DIFF STAT =====")
    result = subprocess.run(["git", "diff", "--stat"], cwd=REPO_ROOT)
    if result.returncode != 0:
        print("STOP: diff stat failed.")
        sys.exit(result.returncode)

    run(["git", "add", "-A"], "STAGE")

    print("===== CHECK FOR CHANGES =====")
    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=REPO_ROOT,
    )
    if result.returncode == 0:
        print("STOP: no changes to commit.")
        sys.exit(0)
    if result.returncode != 1:
        print("STOP: could not determine staged changes.")
        sys.exit(result.returncode)

    run(["git", "diff", "--cached", "--check"], "STAGED DIFF CHECK")

    print("===== STAGED DIFF STAT =====")
    result = subprocess.run(
        ["git", "diff", "--cached", "--stat"],
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        print("STOP: staged diff stat failed.")
        sys.exit(result.returncode)

    run(["git", "commit", "-m", commit_message], "COMMIT")

    run(["git", "push"], "PUSH")

    print("===== COMPLETE =====")
    run(["git", "status", "--short"], "FINAL STATUS")


if __name__ == "__main__":
    main()
