import inspect

from pylage.ENGINE.runtime import GranianRuntime


def test_granian_runtime_constructor_contract():
    signature = inspect.signature(GranianRuntime)

    assert "factory_path" in signature.parameters
    assert "host" in signature.parameters
    assert "port" in signature.parameters


def test_granian_runtime_lifecycle_contract():
    assert hasattr(GranianRuntime, "start")
    assert hasattr(GranianRuntime, "stop")
    assert hasattr(GranianRuntime, "url")
    assert hasattr(GranianRuntime, "running")
