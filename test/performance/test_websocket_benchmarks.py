import asyncio
import time

from pylage.ENGINE import Column, Heading, State
from pylage.ENGINE.core.protocol_codec import decode_message
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_phase6_websocket_state_update_latency():
    async def run():
        count = State(0)
        heading = Heading(text=count)
        app = Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                samples = 100

                start = time.perf_counter()

                for value in range(1, samples + 1):
                    count.set(value)

                    raw = await asyncio.wait_for(
                        ws.recv(),
                        timeout=2,
                    )

                    message = decode_message(raw).to_dict()

                    assert message["type"] == "update"
                    assert message["id"] == heading.id
                    assert message["props"]["text"] == value

                elapsed = time.perf_counter() - start

                print("\n===== PHASE 6 — WEBSOCKET STATE UPDATE =====")
                print(f"iterations        : {samples}")
                print(f"total             : {elapsed:.9f}s")
                print(f"per update        : {elapsed / samples:.9f}s")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_tree_patch_latency():
    async def run():
        root = Column()
        server = WebSocketServer(root)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                samples = 100

                start = time.perf_counter()

                for index in range(samples):
                    child = Heading(text=f"item-{index}")
                    root.add(child)

                    raw = await asyncio.wait_for(
                        ws.recv(),
                        timeout=2,
                    )

                    message = decode_message(raw).to_dict()

                    assert message["type"] == "tree_add"
                    assert message["parent_id"] == root.id

                elapsed = time.perf_counter() - start

                print("\n===== PHASE 6 — WEBSOCKET TREE PATCH =====")
                print(f"iterations        : {samples}")
                print(f"total             : {elapsed:.9f}s")
                print(f"per patch         : {elapsed / samples:.9f}s")

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_multi_client_broadcast():
    async def run():
        count = State(0)
        heading = Heading(text=count)
        app = Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            client_count = 10

            connections = [
                await websockets.connect(url)
                for _ in range(client_count)
            ]

            try:
                start = time.perf_counter()

                count.set(1)

                messages = await asyncio.gather(
                    *[
                        asyncio.wait_for(
                            ws.recv(),
                            timeout=2,
                        )
                        for ws in connections
                    ]
                )

                elapsed = time.perf_counter() - start

                for raw in messages:
                    message = decode_message(raw).to_dict()

                    assert message["type"] == "update"
                    assert message["id"] == heading.id
                    assert message["props"]["text"] == 1

                print("\n===== PHASE 6 — WEBSOCKET BROADCAST =====")
                print(f"clients            : {client_count}")
                print(f"total              : {elapsed:.9f}s")
                print(f"per client         : {elapsed / client_count:.9f}s")

            finally:
                await asyncio.gather(
                    *(ws.close() for ws in connections)
                )

        finally:
            server.stop()

    asyncio.run(run())


def test_phase6_websocket_client_scaling():
    async def run():
        for client_count in (10, 50, 100):
            count = State(0)
            heading = Heading(text=count)
            app = Column(heading)

            server = WebSocketServer(app)

            try:
                url = server.start()

                import websockets

                connections = [
                    await websockets.connect(url)
                    for _ in range(client_count)
                ]

                try:
                    start = time.perf_counter()

                    count.set(1)

                    messages = await asyncio.gather(
                        *[
                            asyncio.wait_for(
                                ws.recv(),
                                timeout=5,
                            )
                            for ws in connections
                        ]
                    )

                    elapsed = time.perf_counter() - start

                    assert len(messages) == client_count

                    for raw in messages:
                        message = decode_message(raw).to_dict()
                        assert message["type"] == "update"
                        assert message["id"] == heading.id
                        assert message["props"]["text"] == 1

                    print("\n===== PHASE 6 — WEBSOCKET CLIENT SCALING =====")
                    print(f"clients            : {client_count}")
                    print(f"total              : {elapsed:.9f}s")
                    print(f"per client         : {elapsed / client_count:.9f}s")

                finally:
                    await asyncio.gather(
                        *(ws.close() for ws in connections)
                    )

            finally:
                server.stop()

    asyncio.run(run())


def test_phase12_websocket_chart_multi_session_benchmark():
    async def run():
        import websockets
        import plotly.graph_objects as go

        from pylage import Chart

        for client_count in (10, 50, 100):
            chart_state = State(
                go.Figure(
                    data=[
                        go.Scatter(
                            x=list(range(100)),
                            y=list(range(100)),
                            mode="lines",
                            name="initial",
                        )
                    ]
                )
            )

            chart = Chart(chart_state)
            app = Column(chart)
            server = WebSocketServer(app)

            try:
                url = server.start()

                connections = [
                    await websockets.connect(url)
                    for _ in range(client_count)
                ]

                try:
                    updated_figure = go.Figure(
                        data=[
                            go.Scatter(
                                x=list(range(120)),
                                y=list(range(120)),
                                mode="lines",
                                name="updated",
                            )
                        ]
                    )

                    start = time.perf_counter()

                    chart_state.set(updated_figure)

                    messages = await asyncio.gather(
                        *[
                            asyncio.wait_for(
                                ws.recv(),
                                timeout=5,
                            )
                            for ws in connections
                        ]
                    )

                    elapsed = time.perf_counter() - start

                    assert len(messages) == client_count

                    for raw in messages:
                        message = decode_message(raw).to_dict()

                        assert message["type"] == "update"
                        assert message["id"] == chart.id
                        assert "props" in message
                        assert "_chart_payload" in message["props"]

                    print()
                    print(
                        "===== PHASE 12 — WEBSOCKET CHART "
                        "SIMULTANEOUS SESSIONS ====="
                    )
                    print(f"clients            : {client_count}")
                    print(f"total              : {elapsed:.9f}s")
                    print(f"per client         : {elapsed / client_count:.9f}s")

                finally:
                    await asyncio.gather(
                        *(ws.close() for ws in connections)
                    )

            finally:
                server.stop()

    asyncio.run(run())
