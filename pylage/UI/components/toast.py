from __future__ import annotations

from typing import Any

from pylage.ENGINE import Style
from pylage.ENGINE import Text as _Text
from pylage.ENGINE import Toast as _Toast
from pylage.ENGINE.core.component import Component


__all__ = ["toast"]


_VARIANT_STYLES: dict[str, Style] = {
    "default": Style(
        background_color="var(--color-surface-variant)",
        color="var(--color-text)",
        border="1px solid " + "var(--color-border)",
    ),
    "info": Style(
        background_color="var(--color-info)",
        color="var(--color-primary-contrast)",
        border="1px solid " + "var(--color-info)",
    ),
    "success": Style(
        background_color="var(--color-success)",
        color="var(--color-primary-contrast)",
        border="1px solid " + "var(--color-success)",
    ),
    "warning": Style(
        background_color="var(--color-warning)",
        color="var(--color-text)",
        border="1px solid " + "var(--color-warning)",
    ),
    "danger": Style(
        background_color="var(--color-danger)",
        color="var(--color-primary-contrast)",
        border="1px solid " + "var(--color-danger)",
    ),
    "error": Style(
        background_color="var(--color-danger)",
        color="var(--color-primary-contrast)",
        border="1px solid " + "var(--color-danger)",
    ),
}


_BASE_STYLE = Style(
    display="flex",
    flex_direction="column",
    gap="var(--spacing-xs)",
    padding="var(--spacing-md)",
    border_radius="var(--radius-md)",
)


def toast(
    *children: Any,
    variant: str = "default",
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit toast using the existing PyLage Toast."""
    if variant not in _VARIANT_STYLES:
        valid = ", ".join(_VARIANT_STYLES)
        raise ValueError(
            f"Unknown toast variant {variant!r}. Expected one of: {valid}."
        )

    final_style = _BASE_STYLE.merge(_VARIANT_STYLES[variant]).merge(style)

    normalized_children = [
        child if isinstance(child, Component) else _Text(child)
        for child in children
        if child is not None
    ]

    return _Toast(*normalized_children, style=final_style, **props)
