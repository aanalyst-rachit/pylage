import asyncio

import pylage as ps
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
