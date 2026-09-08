from typing import Any
from pylage.ENGINE.components.basic import Row as _Row
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.styling.responsive import ResponsiveStyle
from ._common import default_responsive_style
from ._shorthand import build_layout_style

__all__ = ["row"]

def row(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component:
    """Create a UI Kit row using the existing PyLage Row component."""
    normalized_children = [child for child in children if child is not None]
    responsive = props.pop("responsive", None)
    return _Row(*normalized_children, style=build_layout_style(default_responsive_style(), props, responsive=responsive, style=style), **props)
