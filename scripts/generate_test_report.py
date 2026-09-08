from pathlib import Path
from collections import defaultdict
from datetime import datetime
import subprocess
import time

import pytest


ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "test"
REPORT_DIR = TEST_DIR / "reports"


CATEGORIES = (
    "foundation",
    "components",
    "reactive",
    "browser",
    "websocket",
    "integration",
    "performance",
    "regression",
)


class RegressionReporter:
    def __init__(self):
        self.tests = {}
        self.collection_errors = []
        self.start_time = time.perf_counter()

    def pytest_collectreport(self, report):
        if report.failed:
            self.collection_errors.append(str(report.nodeid))

    def pytest_runtest_logreport(self, report):
        if report.when not in ("setup", "call", "teardown"):
            return

        result = self.tests.setdefault(
            report.nodeid,
            {"outcome": "passed", "duration": 0.0, "stdout": ""},
        )

        result["duration"] += report.duration

        if report.when == "call":
            captured = getattr(report, "capstdout", "") or ""
            if captured.strip():
                result["stdout"] = captured.strip()

        if report.failed:
            result["outcome"] = "failed"
        elif report.skipped and result["outcome"] != "failed":
            result["outcome"] = "skipped"


def get_category(nodeid):
    parts = Path(nodeid.split("::", 1)[0]).parts
    try:
        index = parts.index("test")
        category = parts[index + 1]
        if category in CATEGORIES:
            return category
    except (ValueError, IndexError):
        pass
    return "other"


def git_value(*args):
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return "unknown"


def write_report(reporter, exit_code):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    duration = time.perf_counter() - reporter.start_time
    timestamp = datetime.now().astimezone()
    commit = git_value("rev-parse", "HEAD")
    branch = git_value("branch", "--show-current")

    counts = defaultdict(int)
    category_counts = defaultdict(lambda: defaultdict(int))
    category_duration = defaultdict(float)

    for nodeid, result in reporter.tests.items():
        outcome = result["outcome"]
        category = get_category(nodeid)
        counts["total"] += 1
        counts[outcome] += 1
        category_counts[category]["total"] += 1
        category_counts[category][outcome] += 1
        category_duration[category] += result["duration"]

    overall = "PASS" if exit_code == 0 and not reporter.collection_errors else "FAIL"

    report_name = timestamp.strftime("regression_%Y%m%d_%H%M%S.md")
    report_path = REPORT_DIR / report_name

    slowest = sorted(
        reporter.tests.items(),
        key=lambda item: item[1]["duration"],
        reverse=True,
    )[:10]

    performance_tests = [
        (nodeid, result)
        for nodeid, result in reporter.tests.items()
        if get_category(nodeid) == "performance"
    ]
    performance_tests.sort(
        key=lambda item: item[1]["duration"],
        reverse=True,
    )

    lines = [
        "# TEST REGRESSION REPORT",
        "",
        f"Run Date: {timestamp.isoformat()}",
        f"Commit: {commit}",
        f"Branch: {branch}",
        f"Overall Result: {overall}",
        f"Total Tests: {counts["total"]}",
        f"Passed: {counts["passed"]}",
        f"Failed: {counts["failed"]}",
        f"Skipped: {counts["skipped"]}",
        f"Duration: {duration:.2f}s",
        "",
        "## CATEGORY SUMMARY",
        "",
        "| Category | Tests | Passed | Failed | Skipped | Test Duration |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for category in CATEGORIES:
        values = category_counts[category]
        lines.append(
            f"| {category} | {values["total"]} | "
            f"{values["passed"]} | {values["failed"]} | "
            f"{values["skipped"]} | {category_duration[category]:.2f}s |"
        )

    lines.extend([
        "",
        "## KEY HIGHLIGHTS",
        "",
        f"- Full suite exit status: {exit_code}",
        f"- {counts["passed"]} tests passed.",
        f"- {counts["failed"]} tests failed.",
        f"- {counts["skipped"]} tests skipped.",
        f"- {counts["total"]} tests were executed.",
    ])

    if reporter.collection_errors:
        lines.append(f"- Collection errors: {len(reporter.collection_errors)}")
        for error in reporter.collection_errors:
            lines.append(f"  - {error}")

    lines.extend(["", "### Slowest Tests", ""])

    for nodeid, result in slowest:
        lines.append(
            f"- `{nodeid}` — {result["duration"]:.3f}s — {result["outcome"]}"
        )

    fence = chr(96) * 3

    lines.extend([
        "",
        "## PERFORMANCE HIGHLIGHTS",
        "",
        "- Component creation overhead",
        "- Render overhead",
        "- State update overhead",
        "- WebSocket update behavior",
        "- Unnecessary tree changes",
        "- Large dashboard behavior",
        "- Large table behavior",
        "- Repeated component creation",
        "- Client and bundle impact",
        "",
        "### Performance Test Durations",
        "",
    ])

    for nodeid, result in performance_tests:
        lines.append(
            f"- {fence}{nodeid}{fence} — {result["duration"]:.3f}s — {result["outcome"]}"
        )
        stdout = result.get("stdout", "").strip()
        if stdout:
            lines.extend([
                "",
                "  **Benchmark output:**",
                "",
                f"  {fence}text",
            ])
            for output_line in stdout.splitlines():
                lines.append(f"  {output_line}" if output_line else "")
            lines.append(f"  {fence}")

    lines.extend([
        "",
        "## FINAL STATUS",
        "",
        f"**{overall}**",
        "",
        "END OF REPORT",
        "",
    ])

    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    reporter = RegressionReporter()

    print("=== FULL REGRESSION ===")
    print("Running pytest test/ once...")
    print()

    exit_code = pytest.main(
        [str(TEST_DIR), "-q"],
        plugins=[reporter],
    )

    report_path = write_report(reporter, exit_code)

    print()
    print("=== REGRESSION REPORT ===")
    print(f"Report: {report_path}")
    print(f"Exit code: {exit_code}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
