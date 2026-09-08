from typing import Any
from pylage.ENGINE.components.basic import Drawer as PDrawer
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle


def Drawer(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return PDrawer(*children, style=style, **props)


def NavigationDrawer(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return PDrawer(*children, style=style, **props)


def MobileSidebar(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return PDrawer(*children, style=style, **props)


__all__ = ["Drawer", "NavigationDrawer", "MobileSidebar"]
