import threading
import time
import urllib.request
import json

import pyskin as ps
from pyskin.runtime import Runtime


print("=== PYSKIN BROWSER REACTIVE COUNTER TEST ===")

count = ps.State(0)
clicked = threading.Event()


def increment():
    count.set(count.value + 1)
    clicked.set()
    return count.value


heading = ps.Heading(count)

button = ps.Button(
    "Increment",
    on_click=increment,
)

app = ps.Column(
    heading,
    button,
)

runtime = Runtime(
    app,
    title="PySkin Reactive Counter",
    output="browser_reactive_counter/index.html",
)

try:
    url = runtime.start()

    print("HTTP:", url)
    print("WebSocket:", runtime._websocket.url)
    print("Heading ID:", heading.id)
    print("Button ID:", button.id)
    print("Initial state:", count.value)

    with urllib.request.urlopen(url, timeout=2) as response:
        html = response.read().decode("utf-8")

    assert f'data-pyskin-id="{heading.id}"' in html
    assert f'data-pyskin-id="{button.id}"' in html
    assert "Increment" in html

    print("HTML checks: PASS")

    print()
    print("OPEN THIS URL IN YOUR BROWSER:")
    print(url)
    print()
    print("Click 'Increment' three times.")
    print("Waiting for Python callbacks...")

    for expected in (1, 2, 3):
        clicked.clear()

        if not clicked.wait(timeout=10):
            raise AssertionError(
                f"Python callback not received for click {expected}."
            )

        assert count.value == expected

        print(
            f"Click {expected}: Python State = {count.value}"
        )

        if expected < 3:
            time.sleep(0.5)

    print()
    print("Browser → WebSocket event: PASS")
    print("WebSocket → Python callback: PASS")
    print("Python callback → State.set(): PASS")
    print("State value sequence 1 → 2 → 3: PASS")
    print()
    print("=== BROWSER REACTIVE COUNTER PASS ===")

finally:
    runtime.stop()
    print("Runtime stopped.")
