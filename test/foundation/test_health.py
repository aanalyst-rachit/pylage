import asyncio
import json
from pathlib import Path
from urllib.request import urlopen

import pylage as pl

from pylage.ENGINE.runtime.asgi import ASGIApp
from pylage.ENGINE.runtime.server import LocalServer


def run(coro):
    return asyncio.run(coro)


def _header(messages, name):
    target = name.lower().encode('latin-1')
    for key, value in messages[0]['headers']:
        if key.lower() == target:
            return value.decode('latin-1')
    return None


def test_local_server_health_endpoint(tmp_path: Path):
    server = LocalServer(tmp_path)
    server.start()

    try:
        with urlopen(f'{server.url}health') as response:
            body = response.read()

        assert response.status == 200
        assert json.loads(body) == {'status': 'ok'}
        assert response.headers['Content-Type'] == 'application/json'
        assert response.headers['Cache-Control'] == 'no-cache'
        assert response.headers['Content-Length'] == str(len(body))
    finally:
        server.stop()


def test_local_server_health_does_not_require_static_file(tmp_path: Path):
    server = LocalServer(tmp_path)
    server.start()

    try:
        with urlopen(f'{server.url}health') as response:
            assert response.status == 200
            assert response.read() == b'{"status":"ok"}'
    finally:
        server.stop()


def test_asgi_health_endpoint():
    app = pl.column(pl.heading('Health Test'))
    asgi = ASGIApp(app, document='<html></html>')
    messages = []

    async def receive():
        return {'type': 'http.request', 'body': b'', 'more_body': False}

    async def send(message):
        messages.append(message)

    run(asgi({'type': 'http', 'path': '/health', 'method': 'GET', 'headers': []}, receive, send))

    assert messages[0]['status'] == 200
    assert json.loads(messages[1]['body']) == {'status': 'ok'}
    assert _header(messages, 'content-type') == 'application/json'
    assert _header(messages, 'cache-control') == 'no-cache'
    assert _header(messages, 'content-length') == str(len(messages[1]['body']))


def test_asgi_health_precedes_static_directory(tmp_path: Path):
    (tmp_path / 'health').write_text('not the health response')
    app = pl.column(pl.heading('Health Test'))
    asgi = ASGIApp(app, directory=tmp_path)
    messages = []

    async def receive():
        return {'type': 'http.request', 'body': b'', 'more_body': False}

    async def send(message):
        messages.append(message)

    run(asgi({'type': 'http', 'path': '/health', 'method': 'GET', 'headers': []}, receive, send))

    assert messages[0]['status'] == 200
    assert messages[1]['body'] == b'{"status":"ok"}'
