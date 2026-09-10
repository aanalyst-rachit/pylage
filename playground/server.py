from __future__ import annotations

import time
import webbrowser

from pylage.ENGINE.runtime import Runtime

from playground.app import get_app
from playground.runtime import inject_playground_bridge


def main() -> None:
    runtime = Runtime(
        get_app(),
        title="PyLage Playground",
        output="index.html",
        host="127.0.0.1",
        port=8000,
        document_transform=inject_playground_bridge,
    )

    url = runtime.start()
    print(f"PyLage Playground running at {url}")
    print("Press Ctrl+C to stop.")

    webbrowser.open(url)

    try:
        while True:
            time.sleep(0.25)
    except KeyboardInterrupt:
        print("\nStopping PyLage Playground...")
    finally:
        runtime.stop()


if __name__ == "__main__":
    main()
