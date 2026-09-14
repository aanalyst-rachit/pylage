import inspect
from unittest.mock import patch

import pytest

from pylage.ENGINE.runtime import GranianRuntime
from pylage.ENGINE.runtime import granian as granian_runtime


def test_granian_runtime_constructor_contract():
    signature = inspect.signature(GranianRuntime)

    assert "factory_path" in signature.parameters
    assert "host" in signature.parameters
    assert "port" in signature.parameters


def test_granian_runtime_loop_contract():
    default_runtime = GranianRuntime("test.foundation.granian_factory_smoke:create_test_app")
    asyncio_runtime = GranianRuntime("test.foundation.granian_factory_smoke:create_test_app", loop="asyncio")
    uvloop_runtime = GranianRuntime("test.foundation.granian_factory_smoke:create_test_app", loop="uvloop")

    assert default_runtime.loop is None
    assert asyncio_runtime.loop == "asyncio"
    assert uvloop_runtime.loop == "uvloop"


def test_granian_runtime_loop_command_contract():
    class FakeProcess:
        returncode = None

        def poll(self):
            return None

        def terminate(self):
            pass

        def wait(self, timeout=None):
            pass

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    for loop, expected in ((None, None), ("asyncio", "asyncio"), ("uvloop", "uvloop")):
        captured = {}

        def fake_popen(command, captured=captured, **kwargs):
            captured["command"] = command
            return FakeProcess()

        runtime = GranianRuntime(
            "test.foundation.granian_factory_smoke:create_test_app",
            loop=loop,
        )

        with patch.object(granian_runtime.subprocess, "Popen", side_effect=fake_popen), patch.object(
            granian_runtime, "urlopen", return_value=FakeResponse()
        ):
            runtime.start()

        command = captured["command"]
        if expected is None:
            assert "--loop" not in command
        else:
            assert command[-2:] == ["--loop", expected]

        runtime.stop()


def test_granian_runtime_lifecycle_contract():
    assert hasattr(GranianRuntime, "start")
    assert hasattr(GranianRuntime, "stop")
    assert hasattr(GranianRuntime, "url")
    assert hasattr(GranianRuntime, "running")


def test_granian_runtime_tls_constructor_contract():
    runtime = GranianRuntime(
        "test.foundation.granian_factory_smoke:create_test_app",
        ssl_certificate="server.crt",
        ssl_keyfile="server.key",
        ssl_keyfile_password="secret",
    )

    assert runtime.ssl_certificate == "server.crt"
    assert runtime.ssl_keyfile == "server.key"
    assert runtime.ssl_keyfile_password == "secret"


def test_granian_runtime_tls_requires_certificate_and_key():
    factory = "test.foundation.granian_factory_smoke:create_test_app"

    with pytest.raises(ValueError, match="must be provided together"):
        GranianRuntime(factory, ssl_certificate="server.crt")

    with pytest.raises(ValueError, match="must be provided together"):
        GranianRuntime(factory, ssl_keyfile="server.key")


def test_granian_runtime_tls_command_contract():
    class FakeProcess:
        returncode = None

        def poll(self):
            return None

        def terminate(self):
            pass

        def wait(self, timeout=None):
            pass

    class FakeResponse:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    captured = {}

    def fake_popen(command, **kwargs):
        captured["command"] = command
        return FakeProcess()

    runtime = GranianRuntime(
        "test.foundation.granian_factory_smoke:create_test_app",
        ssl_certificate="server.crt",
        ssl_keyfile="server.key",
        ssl_keyfile_password="secret",
    )

    with patch.object(granian_runtime.subprocess, "Popen", side_effect=fake_popen), patch.object(
        granian_runtime, "urlopen", return_value=FakeResponse()
    ):
        started_url = runtime.start()

    command = captured["command"]
    assert command[-6:] == [
        "--ssl-certificate",
        "server.crt",
        "--ssl-keyfile",
        "server.key",
        "--ssl-keyfile-password",
        "secret",
    ]
    assert started_url.startswith("https://127.0.0.1:")
    assert runtime.url.startswith("https://127.0.0.1:")
    runtime.stop()


def test_embedded_granian_runtime_constructor_contract():
    from pylage.ENGINE.runtime import EmbeddedGranianRuntime
    from pylage.ENGINE.runtime.asgi import ASGIApp

    def app_factory():
        from pylage import column, heading
        return column(heading("Embedded Test"))

    application = ASGIApp(app_factory=app_factory)
    runtime = EmbeddedGranianRuntime(application, host="127.0.0.1", port=8124)

    assert runtime.application is application
    assert runtime.host == "127.0.0.1"
    assert runtime.port == 8124
    assert runtime.running is False


def test_embedded_granian_runtime_requires_explicit_port():
    from pylage.ENGINE.runtime import EmbeddedGranianRuntime
    from pylage.ENGINE.runtime.asgi import ASGIApp

    def app_factory():
        from pylage import column
        return column()

    application = ASGIApp(app_factory=app_factory)

    with pytest.raises(ValueError, match="explicit non-zero port"):
        EmbeddedGranianRuntime(application, port=0)


def test_embedded_granian_runtime_rejects_invalid_application():
    from pylage.ENGINE.runtime import EmbeddedGranianRuntime

    with pytest.raises(TypeError, match="must be an ASGIApp"):
        EmbeddedGranianRuntime(object())


def test_embedded_granian_runtime_real_lifecycle():
    from pylage.ENGINE.runtime import EmbeddedGranianRuntime
    from pylage.ENGINE.runtime.asgi import ASGIApp

    def app_factory():
        from pylage import column, heading
        return column(heading("Embedded Lifecycle"))

    application = ASGIApp(app_factory=app_factory)
    runtime = EmbeddedGranianRuntime(application, host="127.0.0.1", port=8125)

    try:
        url = runtime.start()

        assert url == "http://127.0.0.1:8125/"
        assert runtime.url == url
        assert runtime.running is True
    finally:
        runtime.stop()

    assert runtime.running is False
    with pytest.raises(RuntimeError, match="not running"):
        _ = runtime.url
