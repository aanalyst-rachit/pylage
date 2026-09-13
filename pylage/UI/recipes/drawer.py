"""Reusable UI Kit drawer recipes."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style
from pylage.UI.layout.drawer import (
    Drawer as _Drawer,
)
from pylage.UI.layout.drawer import (
    MobileSidebar as _MobileSidebar,
)
from pylage.UI.layout.drawer import (
    NavigationDrawer as _NavigationDrawer,
)

__all__ = ["drawer", "mobile_sidebar", "navigation_drawer"]


def drawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    **props: Any,
) -> Component:
    """Return the existing PyLage Drawer through the UI Kit recipe API."""
    return _Drawer(*children, style=style, **props)


def navigation_drawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    **props: Any,
) -> Component:
    """Return the existing navigation drawer through the UI Kit API."""
    return _NavigationDrawer(*children, style=style, **props)


def mobile_sidebar(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    **props: Any,
) -> Component:
    """Return the existing mobile sidebar through the UI Kit API."""
    return _MobileSidebar(*children, style=style, **props)
