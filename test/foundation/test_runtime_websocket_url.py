import re

from pylage.ENGINE import Column, Text
from pylage.ENGINE.runtime.runtime import Runtime
from pylage.ENGINE import Column, Text


def test_runtime_rewrites_wildcard_websocket_host_for_browser():
    app = Column(
        Text("WebSocket URL test"),
    )

    runtime = Runtime(
        app,
        host="0.0.0.0",
        port=0,
    )

    try:
        runtime.start()

        html = runtime.output.read_text(encoding="utf-8")

        assert "window.PyLage.websocketUrl" in html

        match = re.search(
            r'window\.PyLage\.websocketUrl\s*=\s*["\']([^"\']+)["\']',
            html,
        )

        assert match is not None

        websocket_url = match.group(1)

        assert websocket_url.startswith("ws://")
        assert "0.0.0.0" not in websocket_url
        assert websocket_url.endswith(f":{runtime._websocket.port}/")

    finally:
        runtime.stop()
