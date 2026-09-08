from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Badge as _Badge
from pylage.ENGINE.components.basic import Text as _Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style


_VARIANT_STYLES: dict[str, Style] = {
    "default": Style(
        background_color="var(--color-surface-variant)",
        color="var(--color-text)",
        border="1px solid var(--color-border)",
    ),
    "primary": Style(
        background_color="var(--color-primary)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-primary)",
    ),
    "secondary": Style(
        background_color="var(--color-secondary)",
        color="var(--color-secondary-contrast)",
        border="1px solid var(--color-secondary)",
    ),
    "success": Style(
        background_color="var(--color-success)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-success)",
    ),
    "warning": Style(
        background_color="var(--color-warning)",
        color="var(--color-text)",
        border="1px solid var(--color-warning)",
    ),
    "danger": Style(
        background_color="var(--color-danger)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-danger)",
    ),
    "info": Style(
        background_color="var(--color-info)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-info)",
    ),
}

_BASE_STYLE = Style(
    padding="0.25rem 0.625rem",
    border_radius="var(--radius-full)",
    font_size="0.75rem",
    font_weight="600",
)


def badge(
    *children: Any,
    variant: str = "default",
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit badge using the existing PyLage Badge."""
    if variant not in _VARIANT_STYLES:
        valid = ", ".join(_VARIANT_STYLES)
        raise ValueError(
            f"Unknown badge variant {variant!r}. Expected one of: {valid}."
        )

    default_style = _BASE_STYLE.merge(_VARIANT_STYLES[variant])
    final_style = default_style.merge(style)

    normalized_children = [
        child if isinstance(child, Component) else _Text(child)
        for child in children
        if child is not None
    ]

    return _Badge(*normalized_children, style=final_style, **props)
