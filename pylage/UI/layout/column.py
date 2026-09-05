from typing import Any
from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from ._common import default_responsive_style
from ._shorthand import build_layout_style

__all__ = ["column"]


def column(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    """Create a UI Kit column using the existing PyLage Column component."""
    normalized_children = [child for child in children if child is not None]
    responsive = props.pop("responsive", None)
    return _Column(*normalized_children, style=build_layout_style(default_responsive_style(), props, responsive=responsive, style=style), **props)
