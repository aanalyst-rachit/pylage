import pytest

from pylage.ENGINE import Column, Heading
from pylage.ENGINE.runtime.runtime import Runtime


def test_runtime_reload_app_updates_document_and_root(tmp_path):
    old_app = Column(Heading("Old App"))
    new_app = Column(Heading("New App"))
    output = tmp_path / "index.html"

    runtime = Runtime(old_app, output=output)
    runtime.render()

    assert "Old App" in output.read_text(encoding="utf-8")

    result = runtime.reload_app(new_app)

    assert result == output
    assert runtime.app is new_app
    assert "New App" in output.read_text(encoding="utf-8")
    assert "Old App" not in output.read_text(encoding="utf-8")


def test_runtime_reload_app_rejects_invalid_component(tmp_path):
    runtime = Runtime(Column(Heading("Stable App")), output=tmp_path / "index.html")

    with pytest.raises(TypeError, match="replacement app"):
        runtime.reload_app("not-a-component")


def test_runtime_reload_app_render_failure_preserves_active_app(tmp_path, monkeypatch):
    old_app = Column(Heading("Stable App"))
    new_app = Column(Heading("Replacement App"))
    output = tmp_path / "index.html"

    runtime = Runtime(old_app, output=output)
    runtime.render()
    original_document = output.read_text(encoding="utf-8")

    def fail_render(*args, **kwargs):
        raise RuntimeError("reload render failed")

    import pylage.ENGINE.runtime.runtime as runtime_module

    monkeypatch.setattr(runtime_module, "render_document", fail_render)

    with pytest.raises(RuntimeError, match="reload render failed"):
        runtime.reload_app(new_app)

    assert runtime.app is old_app
    assert output.read_text(encoding="utf-8") == original_document


def test_runtime_reload_app_notifies_running_websocket(tmp_path):
    import asyncio

    import websockets

    from pylage.ENGINE.core.protocol_codec import decode_message
    from pylage.ENGINE.runtime.websocket import WebSocketServer

    async def run():
        old_app = Column(Heading("Old App"))
        new_app = Column(Heading("New App"))
        runtime = Runtime(old_app, output=tmp_path / "index.html")
        server = WebSocketServer(old_app)
        runtime._websocket = server

        try:
            url = server.start()

            async with websockets.connect(url) as ws:
                runtime.reload_app(new_app)

                message = decode_message(
                    await asyncio.wait_for(ws.recv(), timeout=2)
                ).to_dict()

                assert runtime.app is new_app
                assert server.root is new_app
                assert message == {"type": "reload"}
        finally:
            server.stop()

    asyncio.run(run())
