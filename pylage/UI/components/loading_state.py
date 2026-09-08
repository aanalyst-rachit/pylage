from __future__ import annotations

from typing import Any
from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.components.basic import Spinner as _Spinner
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Text as _Text

_DEFAULT_CONTAINER_STYLE = Style(
    display="flex",
    flex_direction="column",
    align_items="center",
    justify_content="center",
    text_align="center",
    padding="var(--spacing-2xl)",
    background_color="var(--color-background)",
    border_radius="var(--radius-xl)",
    gap="var(--spacing-sm)",
)

_TEXT_STYLE = Style(
    font_size="1rem",
    font_weight="500",
    color="var(--color-text)",
    margin="0",
)

_DESC_STYLE = Style(
    font_size="0.875rem",
    color="var(--color-text-muted)",
    max_width="24rem",
    margin="0",
    line_height="1.5",
)

def loading_state(
    text: Any = "Loading...",
    description: Any = None,
    *,
    spinner: bool = True,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit loading state component."""
    items: list[Any] = []

    if spinner:
        items.append(_Spinner())

    if text is not None:
        items.append(_Text(text, style=_TEXT_STYLE))

    if description is not None:
        items.append(_Text(description, style=_DESC_STYLE))

    final_style = _DEFAULT_CONTAINER_STYLE.merge(style)

    return _Column(
        *items,
        style=final_style,
        **props,
    )
