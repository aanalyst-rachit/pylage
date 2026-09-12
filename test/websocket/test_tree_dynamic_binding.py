import asyncio
import json
from pylage.ENGINE.core.protocol_codec import decode_message
import pytest

from pylage.ENGINE import Button, Column, Heading, State
from pylage.ENGINE.runtime.websocket import WebSocketServer


def test_dynamic_component_added_after_server_init_has_event_dispatch():
    root = Column()
    server = WebSocketServer(root)

    clicked = [False]

    def on_click(e=None):
        clicked[0] = True

    new_button = Button("Click Me", on_click=on_click)
    root.add(new_button)

    # Server should index the dynamically added component
    assert server._dispatcher.has_component(new_button.id)

    # Dispatching event should invoke handler without KeyError
    server._dispatcher.dispatch(new_button.id, "click")
    assert clicked[0] is True


def test_dynamic_component_added_after_server_init_receives_state_binding():
    root = Column()
    server = WebSocketServer(root)

    messages = []

    async def fake_broadcast(message, **kwargs):
        messages.append(message)

    server._broadcast = fake_broadcast

    loop = asyncio.new_event_loop()
    server._loop = loop
    server._server = object()

    count = State(10)
    new_heading = Heading(count)
    root.add(new_heading)

    # Trigger state change
    count.set(20)

    # Let scheduler flush
    server._scheduler.flush()
    loop.run_until_complete(asyncio.sleep(0))
    loop.run_until_complete(asyncio.sleep(0.01))

    # The dynamic component should receive update
    updated_props = [
        decode_message(m).to_dict()
        for m in messages
        if decode_message(m).to_dict().get("type") == "update"
        and decode_message(m).to_dict().get("id") == new_heading.id
    ]
    assert len(updated_props) > 0
    assert updated_props[-1]["props"]["text"] == 20

    loop.close()
