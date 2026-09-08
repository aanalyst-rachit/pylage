"""Reusable UI Kit tooltip recipe."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Tooltip as _Tooltip
from pylage.ENGINE.core.component import Component

__all__ = ["tooltip"]


def tooltip(*children: Any, **props: Any) -> Component:
    """Return the existing PyLage Tooltip through the UI Kit recipe API."""
    return _Tooltip(*children, **props)
