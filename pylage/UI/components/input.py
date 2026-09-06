from __future__ import annotations

from typing import Any

from pylage.ENGINE import Input as _Input
from pylage.ENGINE import Style


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
    transition="border-color 150ms ease, box-shadow 150ms ease",
)


def input(
    value: Any = "",
    *,
    input_type: str | None = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI input using the existing engine Input."""
    return _Input(
        value=value,
        input_type=input_type,
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["input"]
