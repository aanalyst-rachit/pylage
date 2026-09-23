import asyncio
import json

from websockets.asyncio.client import connect

from pylage.ENGINE import Column
from pylage.ENGINE.components.chart import Chart
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_chart_event_payload_validation_accepts_valid_events():
    calls = []

    chart = Chart(
        None,
        on_click=lambda payload: calls.append(("click", payload)),
        on_select=lambda payload: calls.append(("select", payload)),
        on_hover=lambda payload: calls.append(("hover", payload)),
        on_relayout=lambda payload: calls.append(("relayout", payload)),
    )

    server = WebSocketServer(Column(chart))
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            messages = [
                {
                    "type": "event",
                    "id": chart.id,
                    "event": "click",
                    "payload": {
                        "points": [
                            {
                                "curveNumber": 0,
                                "pointNumber": 1,
                                "x": 2,
                                "y": 20,
                            }
                        ]
                    },
                },
                {
                    "type": "event",
                    "id": chart.id,
                    "event": "select",
                    "payload": {
                        "points": [],
                        "range": {
                            "x": [1, 3],
                            "y": [10, 30],
                        },
                    },
                },
                {
                    "type": "event",
                    "id": chart.id,
                    "event": "hover",
                    "payload": {
                        "points": [],
                    },
                },
                {
                    "type": "event",
                    "id": chart.id,
                    "event": "relayout",
                    "payload": {
                        "xaxis.range[0]": 1,
                        "xaxis.range[1]": 3,
                    },
                },
            ]

            for message in messages:
                await websocket.send(json.dumps(message))
                response = json.loads(await websocket.recv())
                assert response["ok"] is True

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert [name for name, _ in calls] == [
        "click",
        "select",
        "hover",
        "relayout",
    ]


def test_chart_event_payload_validation_rejects_invalid_payload():
    calls = []

    chart = Chart(
        None,
        on_click=lambda payload: calls.append(payload),
    )

    server = WebSocketServer(Column(chart))
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            message = {
                "type": "event",
                "id": chart.id,
                "event": "click",
                "payload": {
                    "points": "not-a-list",
                },
            }

            await websocket.send(json.dumps(message))
            response = json.loads(await websocket.recv())

            assert response["ok"] is False
            assert "points" in response["error"]

    try:
        asyncio.run(run())
    finally:
        server.stop()

    assert calls == []


def test_websocket_rejects_disallowed_origin():
    server = WebSocketServer(
        Column(Chart(None)),
        allowed_origins=["https://allowed.example"],
    )
    url = server.start()

    async def run():
        try:
            async with connect(
                url,
                origin="https://blocked.example",
            ):
                raise AssertionError("Connection with disallowed origin was accepted")
        except Exception as exc:
            assert "403" in str(exc) or "InvalidOrigin" in type(exc).__name__

    try:
        asyncio.run(run())
    finally:
        server.stop()


def test_websocket_enforces_message_rate_limit():
    chart = Chart(
        None,
        on_click=lambda payload: None,
    )
    server = WebSocketServer(
        Column(chart),
        message_rate_limit=1.0,
        message_rate_burst=1,
    )
    url = server.start()

    async def run():
        async with connect(url) as websocket:
            message = {
                "type": "event",
                "id": chart.id,
                "event": "click",
                "payload": {"points": []},
            }

            await websocket.send(json.dumps(message))
            first = json.loads(await websocket.recv())
            assert first["ok"] is True

            await websocket.send(json.dumps(message))

            try:
                await websocket.recv()
            except Exception as exc:
                assert "1013" in str(exc) or "rate limit" in str(exc).lower()

    try:
        asyncio.run(run())
    finally:
        server.stop()
