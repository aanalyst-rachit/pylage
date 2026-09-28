#!/usr/bin/env python3
"""Prepare and publish a PyLage release."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

VERSION_FILES = {
    Path("pyproject.toml"): (
        re.compile(r'(?m)^version = "[^"]+"$'),
        'version = "{version}"',
    ),
    Path("pylage/__init__.py"): (
        re.compile(r'(?m)^__version__ = "[^"]+"$'),
        '__version__ = "{version}"',
    ),
    Path("pylage/UI/__init__.py"): (
        re.compile(r'(?m)^__version__ = "[^"]+"$'),
        '__version__ = "{version}"',
    ),
    Path("docs/index.md"): (
        re.compile(r"(?m)(PYLAGE )\d+\.\d+\.\d+"),
        r"\g<1>{version}",
    ),
}

SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def run(
    *args: str,
    check: bool = True,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(args))
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        check=check,
        capture_output=capture_output,
    )
    if capture_output:
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
    return result


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run("git", *args, check=check, capture_output=True)


def normalize_version(value: str) -> str:
    version = value.removeprefix("v")
    if not SEMVER_RE.fullmatch(version):
        raise SystemExit(f"Invalid version: {value!r}; expected MAJOR.MINOR.PATCH")
    return version


def validate_commit(commit: str) -> None:
    result = git("rev-parse", "--verify", f"{commit}^{{commit}}", check=False)
    if result.returncode:
        raise SystemExit(f"Commit does not exist: {commit}")

    expected = result.stdout.strip()
    head = git("rev-parse", "HEAD").stdout.strip()

    if head != expected:
        raise SystemExit(
            f"HEAD does not match release commit: HEAD={head}, expected={expected}"
        )


def ensure_tag_available(tag: str) -> None:
    result = git("rev-parse", "--verify", f"refs/tags/{tag}", check=False)
    if result.returncode == 0:
        raise SystemExit(f"Release tag already exists: {tag}")


def require_clean_tree() -> None:
    result = git("status", "--porcelain")
    unexpected = []

    for line in result.stdout.splitlines():
        path = line[3:]
        if path == "helper/release.py" or path == "helper/" or Path(path) in VERSION_FILES:
            continue
        unexpected.append(line)

    if unexpected:
        raise SystemExit(
            "Working tree contains unexpected changes:\n"
            + "\n".join(unexpected)
        )


def rewrite_versions(version: str, dry_run: bool) -> dict[Path, str]:
    original = {}

    for relative, (pattern, replacement) in VERSION_FILES.items():
        path = ROOT / relative
        text = path.read_text()
        updated, count = pattern.subn(
            replacement.format(version=version),
            text,
        )
        if count != 1:
            raise SystemExit(
                f"Expected exactly one version entry in {relative}; found {count}"
            )

        original[path] = text

        if updated == text:
            print(f"unchanged: {relative}")
            continue

        print(f"update: {relative}")
        if not dry_run:
            path.write_text(updated)

    return original


def restore_versions(original: dict[Path, str]) -> None:
    for path, text in original.items():
        path.write_text(text)
    print("release metadata restored after failed validation")


def run_validation(version: str) -> None:
    run(sys.executable, "-m", "ruff", "check", "pylage")
    run(sys.executable, "-m", "pytest", "-q")

    dist = ROOT / "dist"
    if dist.exists():
        shutil.rmtree(dist)

    run(sys.executable, "-m", "build")

    artifacts = sorted(item for item in dist.glob("*") if item.is_file())

    wheel = [
        item
        for item in artifacts
        if item.name.startswith(f"pylage-{version}-") and item.suffix == ".whl"
    ]
    sdist = [
        item
        for item in artifacts
        if item.name == f"pylage-{version}.tar.gz"
    ]

    if len(wheel) != 1 or len(sdist) != 1 or len(artifacts) != 2:
        raise SystemExit(
            "Unexpected build artifacts: "
            f"{[item.name for item in artifacts]}"
        )

    print(f"build artifacts verified: pylage {version}")


def wait_for_docker_http(url: str, timeout: float = 30.0) -> None:
    import time
    import urllib.error
    import urllib.request

    deadline = time.monotonic() + timeout
    last_error = None

    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    print("docker smoke test: HTTP 200")
                    return
        except (OSError, urllib.error.URLError) as exc:
            last_error = exc
        time.sleep(1)

    raise SystemExit(f"Docker smoke test failed: {last_error}")


def run_docker_validation(version: str) -> None:
    image = f"pylage:{version}"
    container = "pylage-release-smoke"

    run("docker", "build", "-t", image, ".")

    cleanup = run(
        "docker",
        "ps",
        "-aq",
        "--filter",
        f"name={container}",
        check=False,
        capture_output=True,
    )
    if cleanup.stdout.strip():
        run("docker", "rm", "-f", container, check=False)

    try:
        run(
            "docker",
            "run",
            "-d",
            "--name",
            container,
            "-p",
            "18080:8000",
            image,
        )
        wait_for_docker_http("http://127.0.0.1:18080/")
    finally:
        run("docker", "rm", "-f", container, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="Release version, e.g. 1.0.8 or v1.0.8")
    parser.add_argument("commit", help="Source commit to release")
    parser.add_argument("--dry-run", action="store_true", help="Validate without changing files")
    parser.add_argument("--execute", action="store_true", help="Create the release commit and tag")
    args = parser.parse_args()

    version = normalize_version(args.version)
    tag = f"v{version}"

    require_clean_tree()
    validate_commit(args.commit)
    ensure_tag_available(tag)

    print(f"release version: {version}")
    print(f"release tag:     {tag}")
    print(f"source commit:   {args.commit}")

    original = rewrite_versions(version, args.dry_run)

    if args.dry_run:
        print("dry-run: no files changed")
        return 0

    try:
        run_validation(version)
        run_docker_validation(version)
    except BaseException:
        restore_versions(original)
        raise

    if not args.execute:
        print("Validation passed. Use --execute to create the release commit and tag.")
        return 0

    git("add", *[str(path) for path in VERSION_FILES])
    git("add", "helper/release.py")
    git("commit", "-m", f"release: v{version}")
    git("tag", "-a", tag, "-m", f"PyLage {tag}")
    git("push", "origin", "HEAD")
    git("push", "origin", tag)

    print(f"Release commit, tag, and push completed: {tag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
