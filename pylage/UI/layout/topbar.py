from typing import Any
from pylage.ENGINE.components.basic import Navigation
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from ._common import resolve_style


def Topbar(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    base_style = Style(
        display="flex",
        align_items="center",
        justify_content="space-between",
        width="100%",
        padding="0.75rem 1.5rem",
    )
    return Navigation(*children, style=resolve_style(style), **props)


__all__ = ["Topbar"]
