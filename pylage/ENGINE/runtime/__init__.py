"""PyLage runtime package.

Runtime implementations are loaded lazily so lightweight modules such as
the HTML renderer and client runtime can be imported without creating a
circular dependency.
"""

__all__ = [
    "Runtime",
    "LocalServer",
    "ASGIApp",
    "create_asgi_app",
    "GranianRuntime",
]


def __getattr__(name: str):
    if name == "Runtime":
        from pylage.ENGINE.runtime.runtime import Runtime
        return Runtime

    if name == "LocalServer":
        from pylage.ENGINE.runtime.server import LocalServer
        return LocalServer

    if name == "ASGIApp":
        from pylage.ENGINE.runtime.asgi import ASGIApp
        return ASGIApp

    if name == "create_asgi_app":
        from pylage.ENGINE.runtime.granian import create_asgi_app
        return create_asgi_app

    if name == "GranianRuntime":
        from pylage.ENGINE.runtime.granian import GranianRuntime
        return GranianRuntime

    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
