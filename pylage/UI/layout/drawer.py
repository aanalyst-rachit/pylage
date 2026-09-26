from typing import Any

from pylage.ENGINE.components.basic import Drawer as PDrawer
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style
from pylage.UI.layout._drawer import normalize_responsive_mode


def Drawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    return PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )


def NavigationDrawer(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    return PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )


def MobileSidebar(
    *children: Any,
    style: Style | ResponsiveStyle | None = None,
    responsive_mode: dict[str, Any] | None = None,
    **props: Any,
) -> Component:
    if responsive_mode is not None:
        responsive_mode = normalize_responsive_mode(responsive_mode)
    return PDrawer(
        *children,
        style=style,
        responsive_mode=responsive_mode,
        **props,
    )


__all__ = ["Drawer", "MobileSidebar", "NavigationDrawer"]
