from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Select as _Select
from pylage.ENGINE.styling.style import Style


_BASE_STYLE = Style(
    width="100%",
    box_sizing="border-box",
    padding="0.625rem 0.75rem",
    font_size="1rem",
    line_height="1.5",
    color="var(--color-text)",
    background_color="var(--color-background)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-md)",
    cursor="pointer",
    transition="border-color 150ms ease, box-shadow 150ms ease",
)


def select(
    *children: Any,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI select using the existing engine Select."""
    return _Select(
        *children,
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["select"]
