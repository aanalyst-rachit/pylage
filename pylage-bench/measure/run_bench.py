#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from common import wait_http


ROOT = Path(__file__).resolve().parent.parent


FRAMEWORKS = {
    "pylage": {
        "cwd": ROOT.parent,
        "command": [
            sys.executable,
            "pylage-bench/apps/counter/pylage_app.py",
        ],
        "url": "http://127.0.0.1:3001/",
    },
    "nicegui": {
        "cwd": ROOT.parent,
        "command": [
            sys.executable,
            "pylage-bench/apps/counter/nicegui_app.py",
        ],
        "url": "http://127.0.0.1:3003/",
    },
    "streamlit": {
        "cwd": ROOT.parent,
        "command": [
            "streamlit",
            "run",
            "pylage-bench/apps/counter/streamlit_app.py",
            "--server.port",
            "3004",
            "--server.headless",
            "true",
        ],
        "url": "http://127.0.0.1:3004/",
    },
    "reflex": {
        "cwd": ROOT / "apps" / "counter" / "reflex_counter",
        "command": [
            "reflex",
            "run",
            "--env",
            "preview",
            "--frontend-port",
            "3005",
        ],
        "url": "http://127.0.0.1:3005/",
    },
}


def stop_process(process):
    if process is None:
        return

    try:
        pgid = os.getpgid(process.pid)
    except ProcessLookupError:
        return

    try:
        os.killpg(pgid, 15)
    except ProcessLookupError:
        return

    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(pgid, 9)
        except ProcessLookupError:
            pass

        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            pass


def run_framework(name, samples, warmup):
    config = FRAMEWORKS[name]

    print()
    print("=" * 60)
    print(f"BENCHMARK: {name}")
    print("=" * 60)
    print("Command:", " ".join(config["command"]))
    print("URL:", config["url"])

    log_dir = ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"counter_{name}.log"

    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            config["command"],
            cwd=config["cwd"],
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

    try:
        print("Waiting for server...")
        wait_http(config["url"], timeout=120.0)

        print("Server ready.")
        print("Running measurement...")

        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "measure" / "run_latency.py"),
                "--name",
                name,
                "--url",
                config["url"],
                "--samples",
                str(samples),
                "--warmup",
                str(warmup),
            ],
            cwd=ROOT.parent,
            check=True,
        )

        return result.returncode

    finally:
        print("Stopping server...")
        stop_process(process)
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--framework",
        choices=[
            "pylage",
            "nicegui",
            "streamlit",
            "reflex",
            "all",
        ],
        default="all",
    )

    parser.add_argument(
        "--samples",
        type=int,
        default=50,
    )

    parser.add_argument(
        "--warmup",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    names = (
        list(FRAMEWORKS)
        if args.framework == "all"
        else [args.framework]
    )

    for name in names:
        run_framework(
            name,
            args.samples,
            args.warmup,
        )


if __name__ == "__main__":
    main()
