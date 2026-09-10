"""PyLage runtime package.

Runtime implementations are loaded lazily so lightweight modules such as
the HTML renderer and client runtime can be imported without creating a
circular dependency.
"""

__all__ = [
    "Runtime",
    "LocalServer",
]


def __getattr__(name: str):
    if name == "Runtime":
        from pylage.ENGINE.runtime.runtime import Runtime
        return Runtime

    if name == "LocalServer":
        from pylage.ENGINE.runtime.server import LocalServer
        return LocalServer

    raise AttributeError(
        f"module {__name__!r} has no attribute {name!r}"
    )
