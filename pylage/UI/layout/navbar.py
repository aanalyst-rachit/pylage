from typing import Any

from pylage.ENGINE.components.basic import Navigation as _Navigation
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from ._common import resolve_style


def navbar(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    base_style = Style(
        display="flex",
        align_items="center",
        justify_content="space-between",
        width="100%",
        padding="1rem 1.5rem",
    )
    resolved_style = base_style.merge(style) if isinstance(style, Style) else resolve_style(style)
    return _Navigation(*children, style=resolved_style, **props)


# Backward-compatible CamelCase alias.
Navbar = navbar


__all__ = ["navbar", "Navbar"]
