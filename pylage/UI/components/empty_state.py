from __future__ import annotations

from typing import Any
from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.components.basic import Heading as _Heading
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
    border="1px dashed var(--color-border-muted)",
    border_radius="var(--radius-xl)",
    gap="var(--spacing-sm)",
)

_TITLE_STYLE = Style(
    font_size="1.125rem",
    font_weight="600",
    color="var(--color-text)",
    margin="0",
)

_DESC_STYLE = Style(
    font_size="0.875rem",
    color="var(--color-text-muted)",
    max_width="28rem",
    margin="0",
    line_height="1.5",
)

_ICON_CONTAINER_STYLE = Style(
    display="inline-flex",
    align_items="center",
    justify_content="center",
    width="3.5rem",
    height="3.5rem",
    border_radius="var(--radius-full)",
    background_color="var(--color-surface)",
    color="var(--color-text-muted)",
    font_size="1.5rem",
    margin_bottom="var(--spacing-xs)",
)

def empty_state(
    title: Any = "No data found",
    description: Any = "There are no items or records to display at this time.",
    *,
    icon: Any = None,
    action: Any = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic, high-level UI Kit empty state card."""
    items: list[Any] = []

    if icon is not None:
        if isinstance(icon, str):
            items.append(_Text(icon, style=_ICON_CONTAINER_STYLE))
        else:
            items.append(icon)

    if title is not None:
        items.append(_Heading(title, style=_TITLE_STYLE))

    if description is not None:
        items.append(_Text(description, style=_DESC_STYLE))

    if action is not None:
        items.append(action)

    final_style = _DEFAULT_CONTAINER_STYLE.merge(style)

    return _Column(
        *items,
        style=final_style,
        **props,
    )
