import asyncio

import pytest

from pylage.ENGINE import Column
from pylage.ENGINE.runtime.websocket import WebSocketServer


class FakeConnection:
    def __init__(self, *, fail_ping=False):
        self.fail_ping = fail_ping
        self.pings = 0
        self.closed = False

    def ping(self):
        self.pings += 1
        if self.fail_ping:
            async def fail():
                raise TimeoutError("pong timeout")
            return fail()
        async def pong():
            return None
        return pong()

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_heartbeat_pings_connections():
    server = WebSocketServer(Column(), heartbeat_interval=0.01)
    connection = FakeConnection()
    server._connections.add(connection)

    task = asyncio.create_task(server._heartbeat())
    await asyncio.sleep(0.035)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    assert connection.pings >= 1
    assert connection in server._connections


@pytest.mark.asyncio
async def test_heartbeat_removes_dead_connections():
    server = WebSocketServer(Column(), heartbeat_interval=0.01)
    connection = FakeConnection(fail_ping=True)
    server._connections.add(connection)

    task = asyncio.create_task(server._heartbeat())
    await asyncio.sleep(0.035)
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)

    assert connection not in server._connections
    assert connection.closed is True


def test_heartbeat_interval_validation():
    with pytest.raises(ValueError, match="heartbeat_interval"):
        WebSocketServer(Column(), heartbeat_interval=0)

    with pytest.raises(ValueError, match="heartbeat_interval"):
        WebSocketServer(Column(), heartbeat_interval=-1)
