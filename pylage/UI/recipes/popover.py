"""Reusable UI Kit popover recipe."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Popover as _Popover
from pylage.ENGINE.core.component import Component

__all__ = ["popover"]


def popover(*children: Any, **props: Any) -> Component:
    """Return the existing PyLage Popover through the UI Kit recipe API."""
    return _Popover(*children, **props)
