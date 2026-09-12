import inspect
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
