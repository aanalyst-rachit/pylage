"""Production end-to-end PyLage comparative benchmark runner."""

from __future__ import annotations

import argparse
import asyncio
import importlib.metadata
import json
import os
import platform
import re
import statistics
import subprocess
import time
import urllib.request
from pathlib import Path

import websockets

from pylage.ENGINE.core.protocol import EventMessage, EventMessageResponse, UpdateMessage
from pylage.ENGINE.core.protocol_codec import decode_message, encode_message


ROOT = Path(__file__).resolve().parents[2]
APP_FILE = Path(__file__).resolve().parent / "app.py"
RESULTS_DIR = Path(__file__).resolve().parent / "results"
BUTTON_MARKER = "Increment"


def read_host_memory() -> dict[str, int | None]:
    values: dict[str, int | None] = {"total_bytes": None, "available_bytes": None}
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal:"):
                values["total_bytes"] = int(line.split()[1]) * 1024
            elif line.startswith("MemAvailable:"):
                values["available_bytes"] = int(line.split()[1]) * 1024
    except (FileNotFoundError, OSError, ValueError):
        pass
    return values


def read_rss_bytes(pid: int) -> int | None:
    status = Path(f"/proc/{pid}/status")
    try:
        for line in status.read_text().splitlines():
            if line.startswith("VmRSS:"):
                return int(line.split()[1]) * 1024
    except (FileNotFoundError, OSError, ValueError):
        return None
    return None


def environment() -> dict[str, object]:
    import pylage

    return {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "pylage": pylage.__version__,
        "granian": importlib.metadata.version("granian"),
        "websockets": websockets.__version__,
    }


def choose_port(host: str) -> int:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def extract_button_id(document: bytes) -> str:
    text = document.decode("utf-8")
    marker = re.escape(BUTTON_MARKER)
    patterns = [
        rf'<button[^>]*data-pylage-id="([^"]+)"[^>]*>[^<]*{marker}[^<]*</button>',
        rf'<[^>]*data-pylage-id="([^"]+)"[^>]*>[^<]*{marker}[^<]*</[^>]+>',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)

    if BUTTON_MARKER not in text:
        raise RuntimeError("Benchmark button marker was not found in the document.")
    raise RuntimeError("Could not associate the benchmark button with a PyLage component ID.")


def wait_until_ready(url: str, process: subprocess.Popen[bytes], started_ns: int, timeout: float = 10.0) -> float:
    deadline = time.perf_counter() + timeout

    while time.perf_counter() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Granian exited during startup with code {process.returncode}.")
        try:
            with urllib.request.urlopen(url, timeout=0.25) as response:
                if response.status < 500:
                    return (time.perf_counter_ns() - started_ns) / 1_000_000
        except OSError:
            time.sleep(0.025)

    raise RuntimeError("Granian did not become ready within 10 seconds.")


def fetch_document(url: str) -> tuple[float, bytes]:
    started = time.perf_counter_ns()
    with urllib.request.urlopen(url, timeout=5) as response:
        document = response.read()
    elapsed = (time.perf_counter_ns() - started) / 1_000_000
    return elapsed, document


async def measure_websocket(url: str, button_id: str, iterations: int, interval: float) -> dict[str, object]:
    latencies_ms: list[float] = []
    update_sizes: list[int] = []

    async with websockets.connect(url) as websocket:
        initial = await asyncio.wait_for(websocket.recv(), timeout=5)
        if not isinstance(initial, str):
            raise RuntimeError("Expected text session frame from the ASGI factory.")
        try:
            session_message = json.loads(initial)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Initial WebSocket frame is not valid JSON.") from exc
        if session_message.get("type") != "session" or not session_message.get("token"):
            raise RuntimeError("Expected a session frame containing a session token.")

        for _ in range(iterations):
            event = EventMessage(component_id=button_id, event="click")
            payload = encode_message(event)
            started = time.perf_counter_ns()
            await websocket.send(payload)

            response_received = False
            while True:
                raw = await asyncio.wait_for(websocket.recv(), timeout=5)
                if not isinstance(raw, (bytes, bytearray, memoryview)):
                    continue
                message = decode_message(raw)

                if isinstance(message, EventMessageResponse):
                    if not message.ok:
                        raise RuntimeError(
                            f"Event dispatch failed: {message.error}"
                        )
                    response_received = True
                    continue

                if isinstance(message, UpdateMessage):
                    if not response_received:
                        raise RuntimeError(
                            "Received UpdateMessage before EventMessageResponse."
                        )
                    elapsed = (time.perf_counter_ns() - started) / 1_000_000
                    latencies_ms.append(elapsed)
                    update_sizes.append(len(raw))
                    break

            await asyncio.sleep(interval)

    ordered = sorted(latencies_ms)
    p95_index = max(0, min(len(ordered) - 1, int(len(ordered) * 0.95) - 1))

    return {
        "iterations": iterations,
        "state_update_latency_ms": {
            "min": min(latencies_ms),
            "mean": statistics.mean(latencies_ms),
            "median": statistics.median(latencies_ms),
            "p95": ordered[p95_index],
            "max": max(latencies_ms),
        },
        "update_payload_bytes": {
            "min": min(update_sizes),
            "mean": statistics.mean(update_sizes),
            "max": max(update_sizes),
        },
    }


def stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is None:
        process.terminate()
        try:
            process.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3.0)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the production PyLage comparative benchmark.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=0)
    parser.add_argument("--iterations", type=int, default=50)
    parser.add_argument("--interval", type=float, default=0.075)
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error("--iterations must be at least 1")
    if args.interval < 0:
        parser.error("--interval must be non-negative")

    port = args.port or choose_port(args.host)
    http_url = f"http://{args.host}:{port}/"
    websocket_url = f"ws://{args.host}:{port}/"

    env = os.environ.copy()
    env["PYLAGE_APP_FILE"] = str(APP_FILE)

    command = [
        str(ROOT / ".venv/bin/granian"),
        "pylage.ENGINE.runtime.granian:create_application_from_file",
        "--interface",
        "asgi",
        "--factory",
        "--host",
        args.host,
        "--port",
        str(port),
    ]

    started_ns = time.perf_counter_ns()
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=env,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        startup_ms = wait_until_ready(http_url, process, started_ns)
        render_ms, document = fetch_document(http_url)
        button_id = extract_button_id(document)
        websocket_result = asyncio.run(
            measure_websocket(websocket_url, button_id, args.iterations, args.interval)
        )
        rss = read_rss_bytes(process.pid)
        host_memory = read_host_memory()

        result = {
            "framework": "pylage",
            "workload": "state-bound heading plus button increment",
            "server": "Granian + ASGI production factory",
            "startup": {
                "definition": "process launch to first HTTP-ready response",
                "latency_ms": startup_ms,
            },
            "initial_render": {
                "latency_ms": render_ms,
                "payload_bytes": len(document),
            },
            "memory": {
                "server_rss_bytes": rss,
            },
            "metrics": websocket_result,
            "throughput": None,
            "environment": {
                **environment(),
                "host_memory": host_memory,
            },
            "benchmark": {
                "iterations": args.iterations,
                "interval_seconds": args.interval,
            },
            "command": command,
        }

        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        output = RESULTS_DIR / "pylage.json"
        output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result, indent=2))
        print(f"RESULT_FILE={output}")
    finally:
        stop_process(process)


if __name__ == "__main__":
    main()
