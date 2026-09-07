from __future__ import annotations

from typing import Any, Callable

from pylage.ENGINE.core.state import DerivedState, State


def derived(*sources: State, compute: Callable[..., Any]) -> State:
    """Create a read-only reactive state derived from source states."""
    return DerivedState(*sources, compute=compute)


__all__ = ["derived"]
