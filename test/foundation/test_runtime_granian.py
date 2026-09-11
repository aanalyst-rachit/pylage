import asyncio
import json
import socket
import subprocess
import time

import websockets


def _free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def test_granian_websocket_event_round_trip():
    port = _free_port()
    command = ['granian', 'test.foundation.granian_event_smoke:create_test_app', '--interface', 'asgi', '--factory', '--host', '127.0.0.1', '--port', str(port)]
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    async def round_trip():
        deadline = time.monotonic() + 10
        last_error = None

        while time.monotonic() < deadline:
            try:
                async with websockets.connect(f"ws://127.0.0.1:{port}/", open_timeout=1) as websocket:
                    message = {"type": "event", "id": "granian-button", "event": "click"}
                    await websocket.send(json.dumps(message, separators=(",", ":")))
                    raw = await asyncio.wait_for(websocket.recv(), timeout=5)
                    return json.loads(raw)
            except (OSError, asyncio.TimeoutError, websockets.WebSocketException) as exc:
                last_error = exc
                await asyncio.sleep(0.1)

        raise AssertionError(f"Granian WebSocket did not become ready: {last_error}")


    try:
        response = asyncio.run(round_trip())
        assert response == {"type": "response", "ok": True}
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
