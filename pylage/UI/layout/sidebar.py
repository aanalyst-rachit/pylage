from typing import Any

from pylage.ENGINE.components.basic import Row
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style
from ._common import resolve_style


def sidebar_layout(
    sidebar: Any = None,
    content: Any = None,
    style: Style | ResponsiveStyle | None = None,
    **props: Any,
) -> Component:
    children = []
    if sidebar is not None:
        children.append(sidebar)
    if content is not None:
        children.append(content)
    return Row(*children, style=resolve_style(style), **props)


# Backward-compatible CamelCase alias.
SidebarLayout = sidebar_layout


__all__ = ["sidebar_layout", "SidebarLayout"]
