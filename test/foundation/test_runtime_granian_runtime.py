import inspect

import pytest
from unittest.mock import patch

from pylage.ENGINE.runtime import GranianRuntime


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

        def fake_popen(command, **kwargs):
            captured["command"] = command
            return FakeProcess()

        runtime = GranianRuntime(
            "test.foundation.granian_factory_smoke:create_test_app",
            loop=loop,
        )

        with patch("pylage.ENGINE.runtime.granian.subprocess.Popen", side_effect=fake_popen), patch(
            "pylage.ENGINE.runtime.granian.urlopen",
            return_value=FakeResponse(),
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

    with patch("pylage.ENGINE.runtime.granian.subprocess.Popen", side_effect=fake_popen), patch(
        "pylage.ENGINE.runtime.granian.urlopen",
        return_value=FakeResponse(),
    ):
        assert runtime.start() == "https://127.0.0.1:0/" or runtime.url.startswith("https://127.0.0.1:")

    command = captured["command"]
    assert command[-6:] == [
        "--ssl-certificate",
        "server.crt",
        "--ssl-keyfile",
        "server.key",
        "--ssl-keyfile-password",
        "secret",
    ]
    assert runtime.url.startswith("https://127.0.0.1:")
    runtime.stop()
