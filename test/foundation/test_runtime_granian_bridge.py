from pylage.ENGINE.core.component import Component
from pylage.ENGINE.runtime.asgi import ASGIApp
from pylage.ENGINE.runtime.granian import load_factory

def test_load_factory_resolves_importable_callable():
    factory = load_factory("test.foundation.test_runtime_asgi:create_granian_smoke_app")
    assert callable(factory)

def test_granian_factory_contract_returns_asgi_app():
    factory = load_factory("test.foundation.test_runtime_asgi:create_granian_smoke_app")
    application = factory()
    assert isinstance(application, ASGIApp)
    assert isinstance(application.root, Component)
