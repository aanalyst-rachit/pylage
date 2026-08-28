from __future__ import annotations

import threading
import time
import urllib.request

import pyskin as ps
from pyskin.runtime import Runtime


event_received = threading.Event()
calls: list[str] = []


def clicked():
    calls.append("clicked")
    print("=== BROWSER EVENT RECEIVED ===")
    event_received.set()
    return "browser-ok"


button = ps.Button(
    "Click me",
    on_click=clicked,
)

app = ps.Column(
    ps.Heading("Browser Event Test"),
    button,
)

runtime = Runtime(
    app,
    title="Browser Event Test",
    output="browser_event_output/index.html",
)

try:
    url = runtime.start()

    print("=== PYSKIN BROWSER EVENT TEST ===")
    print("URL:", url)
    print("Button ID:", button.id)
    print("WebSocket:", runtime._websocket.url)

    with urllib.request.urlopen(url) as response:
        html = response.read().decode("utf-8")

    assert "Browser Event Test" in html
    assert "data-pyskin-events=\"click\"" in html
    assert "websocketUrl" in html

    print("HTML checks: PASS")
    print()
    print("Open this URL in your browser:")
    print(url)
    print()
    print("CLICK THE 'Click me' BUTTON.")
    print("Waiting for Python callback...")

    if not event_received.wait(timeout=30000):
        raise TimeoutError(
            "Browser event was not received within 30 seconds."
        )

    print("Calls:", calls)
    assert calls == ["clicked"]

    print("=== BROWSER EVENT PASS ===")

finally:
    runtime.stop()
    print("Runtime stopped.")
