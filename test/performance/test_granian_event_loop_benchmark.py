import importlib.util
import shutil
import subprocess
import time

import pytest
from urllib.request import urlopen


FACTORY = "test.foundation.granian_factory_smoke:create_test_app"
HOST = "127.0.0.1"
PORT = 8765
WARMUP_REQUESTS = 50
MEASURED_REQUESTS = 500


def _run_granian(loop):
    command = [
        "granian",
        FACTORY,
        "--interface",
        "asgi",
        "--factory",
        "--host",
        HOST,
        "--port",
        str(PORT),
        "--loop",
        loop,
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://{HOST}:{PORT}/"

    try:
        deadline = time.monotonic() + 10.0

        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError(
                    f"Granian exited during startup: {process.returncode}"
                )

            try:
                with urlopen(url, timeout=0.5) as response:
                    if response.status < 500:
                        break
            except OSError:
                time.sleep(0.05)
        else:
            raise RuntimeError("Granian did not become ready within 10 seconds.")

        for _ in range(WARMUP_REQUESTS):
            with urlopen(url, timeout=2.0) as response:
                response.read()

        start = time.perf_counter()
        total_bytes = 0

        for _ in range(MEASURED_REQUESTS):
            with urlopen(url, timeout=2.0) as response:
                total_bytes += len(response.read())

        elapsed = time.perf_counter() - start

        return {
            "loop": loop,
            "requests": MEASURED_REQUESTS,
            "elapsed": elapsed,
            "per_request": elapsed / MEASURED_REQUESTS,
            "requests_per_second": MEASURED_REQUESTS / elapsed,
            "bytes": total_bytes,
        }
    finally:
        process.terminate()

        try:
            process.wait(timeout=3.0)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=3.0)


def test_granian_event_loop_benchmark(capsys):
    if shutil.which("granian") is None:
        pytest.skip("granian executable is not installed")
    if importlib.util.find_spec("uvloop") is None:
        pytest.skip("uvloop is not installed; install pylage[performance]")

    asyncio_result = _run_granian("asyncio")
    uvloop_result = _run_granian("uvloop")

    assert asyncio_result["bytes"] == uvloop_result["bytes"]
    assert asyncio_result["requests"] == uvloop_result["requests"]

    throughput_gain = (
        uvloop_result["requests_per_second"]
        / asyncio_result["requests_per_second"]
        - 1.0
    ) * 100.0

    latency_reduction = (
        (asyncio_result["per_request"] - uvloop_result["per_request"])
        / asyncio_result["per_request"]
    ) * 100.0

    print("===== PY LAGE PHASE 2.4 — GRANIAN EVENT LOOP BENCHMARK =====")
    print(f"warmup requests   : {WARMUP_REQUESTS}")
    print(f"measured requests : {MEASURED_REQUESTS}")
    print()
    print("--- ASYNCIO ---")
    print(f"total             : {asyncio_result["elapsed"]:.9f}s")
    print(f"per request       : {asyncio_result["per_request"]:.9f}s")
    print(f"requests/sec      : {asyncio_result["requests_per_second"]:.3f}")
    print(f"response bytes    : {asyncio_result["bytes"]}")
    print()
    print("--- UVLOOP ---")
    print(f"total             : {uvloop_result["elapsed"]:.9f}s")
    print(f"per request       : {uvloop_result["per_request"]:.9f}s")
    print(f"requests/sec      : {uvloop_result["requests_per_second"]:.3f}")
    print(f"response bytes    : {uvloop_result["bytes"]}")
    print()
    print(f"throughput gain   : {throughput_gain:.2f}%")
    print(f"latency reduction : {latency_reduction:.2f}%")

    captured = capsys.readouterr()
    assert "ASYNCIO" in captured.out
    assert "UVLOOP" in captured.out
