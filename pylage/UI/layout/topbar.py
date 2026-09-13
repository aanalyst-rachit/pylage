from typing import Any

from pylage.ENGINE.components.basic import Navigation
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style

from ._common import resolve_style


def Topbar(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    return Navigation(*children, style=resolve_style(style), **props)


__all__ = ["Topbar"]
