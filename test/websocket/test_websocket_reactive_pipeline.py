import asyncio

from pylage.ENGINE import Column, Heading, State
from pylage.ENGINE.core.protocol_codec import decode_message
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_websocket_state_update_uses_reactive_pipeline():
    async def run():
        count = State(0)

        heading = Heading(text=count)
        app = Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                count.set(1)

                raw = await asyncio.wait_for(
                    ws.recv(),
                    timeout=2,
                )

                message = decode_message(raw).to_dict()

                assert message["type"] == "update"
                assert message["id"] == heading.id
                assert message["props"]["text"] == 1

        finally:
            server.stop()

    asyncio.run(run())

def test_websocket_batches_multiple_state_changes_into_one_final_update():
    async def run():
        count = State(0)

        heading = Heading(text=count)
        app = Column(heading)

        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                count.set(1)
                count.set(2)
                count.set(3)

                raw = await asyncio.wait_for(
                    ws.recv(),
                    timeout=2,
                )

                message = decode_message(raw).to_dict()

                assert message["type"] == "update"
                assert message["id"] == heading.id
                assert message["props"]["text"] == 3

                # There must not be another update for the same
                # synchronous State-change batch.
                try:
                    extra = await asyncio.wait_for(
                        ws.recv(),
                        timeout=0.15,
                    )
                except asyncio.TimeoutError:
                    extra = None

                assert extra is None

        finally:
            server.stop()

    asyncio.run(run())

def test_websocket_metadata_is_cached_per_connection():
    async def run():
        count = State(0)
        heading = Heading(text=count)
        app = Column(heading)
        server = WebSocketServer(app)

        from pylage.ENGINE.core.protocol_codec import decode_message

        try:
            url = server.start()
            import websockets

            async with websockets.connect(url) as ws:
                count.set(1)
                first = decode_message(await asyncio.wait_for(ws.recv(), timeout=2))
                first_dict = first.to_dict()

                assert first_dict['type'] == 'update'
                assert first_dict['id'] == heading.id
                assert first_dict['props']['text'] == 1
                assert 'prop_meta' in first_dict
                assert 'text' in first_dict['prop_meta']

                count.set(2)
                second = decode_message(await asyncio.wait_for(ws.recv(), timeout=2))
                second_dict = second.to_dict()

                assert second_dict['type'] == 'update'
                assert second_dict['id'] == heading.id
                assert second_dict['props']['text'] == 2
                assert 'prop_meta' not in second_dict

            async with websockets.connect(url) as ws:
                count.set(3)
                third = decode_message(await asyncio.wait_for(ws.recv(), timeout=2))
                third_dict = third.to_dict()

                assert third_dict['type'] == 'update'
                assert third_dict['id'] == heading.id
                assert third_dict['props']['text'] == 3
                assert 'prop_meta' in third_dict
                assert 'text' in third_dict['prop_meta']

        finally:
            server.stop()

    asyncio.run(run())


def test_websocket_replace_root_preserves_server_and_uses_new_reactive_pipeline():
    import websockets

    async def run():
        old_count = State(0)
        old_heading = Heading(text=old_count)
        old_app = Column(old_heading)

        new_count = State(10)
        new_heading = Heading(text=new_count)
        new_app = Column(new_heading)

        server = WebSocketServer(old_app)

        try:
            url = server.start()
            original_dispatcher = server._dispatcher
            original_binding = server._binding
            original_observer = server._tree_observer

            async with websockets.connect(url) as ws:
                server.replace_root(new_app)

                assert server.running
                assert server.root is new_app
                assert server._dispatcher is not original_dispatcher
                assert server._binding is not original_binding
                assert server._tree_observer is not original_observer
                assert original_observer._subscriptions == []
                assert original_observer._component_unsubscribers == {}
                assert original_observer._bound_components == set()

                new_count.set(11)

                message = decode_message(
                    await asyncio.wait_for(ws.recv(), timeout=2),
                ).to_dict()

                assert message["type"] == "update"
                assert message["id"] == new_heading.id
                assert message["props"]["text"] == 11

                old_count.set(1)

                try:
                    extra = await asyncio.wait_for(ws.recv(), timeout=0.15)
                except asyncio.TimeoutError:
                    extra = None

                assert extra is None

        finally:
            server.stop()

    asyncio.run(run())


def test_websocket_replace_root_rejects_invalid_component():
    import pytest

    server = WebSocketServer(Column())

    try:
        with pytest.raises(TypeError, match="expects a Component root"):
            server.replace_root("not-a-component")
    finally:
        server.stop()


def test_websocket_notify_reload_preserves_connection():
    async def run():
        app = Column(Heading("Reload Test"))
        server = WebSocketServer(app)

        try:
            url = server.start()

            import websockets

            async with websockets.connect(url) as ws:
                server.notify_reload()

                message = decode_message(
                    await asyncio.wait_for(ws.recv(), timeout=2),
                ).to_dict()

                assert message == {"type": "reload"}
                assert server.running

        finally:
            server.stop()

    asyncio.run(run())