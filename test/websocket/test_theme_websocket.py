import asyncio
import json
from pylage.ENGINE.core.protocol_codec import decode_message

from pylage.ENGINE import Column, Heading
from pylage.ENGINE.runtime.websocket import WebSocketServer
from pylage.ENGINE.styling.global_theme import set_global_theme
from pylage.UI.themes.dark import DARK_THEME
from pylage.UI.themes.light import LIGHT_THEME


async def run_theme_websocket_test():
    set_global_theme(LIGHT_THEME)

    app = Column(
        Heading(text='Theme Test'),
    )

    server = WebSocketServer(app)

    try:
        url = server.start()

        print('=== PYLAGE THEME WEBSOCKET TEST ===')
        print('URL:', url)

        import websockets

        async with websockets.connect(url) as ws:
            print('Connected: PASS')

            set_global_theme(DARK_THEME)

            raw = await asyncio.wait_for(
                ws.recv(),
                timeout=2,
            )

            print('Received:', raw)

            message = decode_message(raw).to_dict()

            assert message['type'] == 'theme_update'
            assert message['css'] == DARK_THEME.to_css()

            print('Message type: PASS')
            print('Theme CSS: PASS')
            print('=== THEME WEBSOCKET PASS ===')

    finally:
        server.stop()
        set_global_theme(LIGHT_THEME)


def test_theme_websocket_update():
    asyncio.run(run_theme_websocket_test())
