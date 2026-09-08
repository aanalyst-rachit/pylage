from __future__ import annotations

from typing import Any

from pylage.ENGINE.core.state import State


_global_theme = State(None)


def set_global_theme(theme: Any) -> None:
    """Set the process-wide active PyLage theme."""
    _global_theme.set(theme)


def get_global_theme() -> Any:
    """Return the process-wide active PyLage theme."""
    return _global_theme.value


def subscribe_global_theme(callback):
    """Subscribe to process-wide theme changes and return an unsubscribe callback."""
    return _global_theme.subscribe(callback)


__all__ = [
    "get_global_theme",
    "set_global_theme",
    "subscribe_global_theme",
]
