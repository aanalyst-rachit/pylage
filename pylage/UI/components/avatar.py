from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Avatar as _Avatar
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Text as _Text
from pylage.ENGINE.core.component import Component

_SIZE_STYLES: dict[str, Style] = {
    "sm": Style(width="32px", height="32px", font_size="0.75rem"),
    "md": Style(width="40px", height="40px", font_size="0.875rem"),
    "lg": Style(width="48px", height="48px", font_size="1rem"),
}

_BASE_STYLE = Style(
    display="inline-flex",
    align_items="center",
    justify_content="center",
    border_radius="9999px",
    overflow="hidden",
    font_weight="600",
)

def avatar(
    *children: Any,
    size: str = "md",
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit avatar using the existing PyLage Avatar."""
    if size not in _SIZE_STYLES:
        valid = ", ".join(_SIZE_STYLES)
        raise ValueError(
            f"Unknown avatar size {size!r}. Expected one of: {valid}."
        )

    final_style = _BASE_STYLE.merge(_SIZE_STYLES[size]).merge(style)

    normalized_children = [
        child if isinstance(child, Component) else _Text(child)
        for child in children
        if child is not None
    ]

    return _Avatar(*normalized_children, style=final_style, **props)
