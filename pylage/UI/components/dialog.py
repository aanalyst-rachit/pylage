from __future__ import annotations

from typing import Any

from pylage.ENGINE import Dialog as _Dialog
from pylage.ENGINE import Style
from pylage.ENGINE.core.component import Component


__all__ = ["dialog"]


_BASE_STYLE = Style(
    padding="var(--spacing-lg)",
    background_color="var(--color-background)",
    color="var(--color-text)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-xl)",
)


def dialog(
    *children: Any,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit dialog using the existing PyLage Dialog."""

    normalized_children = [
        child for child in children
        if child is not None
    ]

    final_style = _BASE_STYLE.merge(style)

    return _Dialog(
        *normalized_children,
        style=final_style,
        **props,
    )
