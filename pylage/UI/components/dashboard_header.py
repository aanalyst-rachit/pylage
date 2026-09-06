from __future__ import annotations

from typing import Any
from pylage.ENGINE import Column as _Column
from pylage.ENGINE import Heading as _Heading
from pylage.ENGINE import Row as _Row
from pylage.ENGINE import Style
from pylage.ENGINE import Text as _Text

_DEFAULT_HEADER_STYLE = Style(
    display="flex",
    flex_direction="row",
    justify_content="space-between",
    align_items="center",
    width="100%",
    padding_bottom="var(--spacing-md)",
    border_bottom="1px solid var(--color-border-muted)",
)

_TITLE_STYLE = Style(
    font_size="1.5rem",
    font_weight="700",
    color="var(--color-text)",
    margin="0",
)

_DESC_STYLE = Style(
    font_size="0.875rem",
    color="var(--color-text-muted)",
    margin="0",
)

def dashboard_header(
    title: Any,
    description: Any = None,
    *,
    actions: Any = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a standardized, responsive header row for dashboards and admin views."""
    text_items = []
    if title is not None:
        if hasattr(title, "type"):
            text_items.append(title)
        else:
            text_items.append(_Heading(title, level=1, style=_TITLE_STYLE))

    if description is not None:
        if hasattr(description, "type"):
            text_items.append(description)
        else:
            text_items.append(_Text(description, style=_DESC_STYLE))

    left_col = _Column(
        *text_items,
        style=Style(display="flex", flex_direction="column", gap="0.25rem"),
    )

    right_side = None
    if actions is not None:
        if isinstance(actions, (list, tuple)):
            right_side = _Row(
                *actions,
                style=Style(display="flex", flex_direction="row", gap="var(--spacing-sm)", align_items="center"),
            )
        else:
            right_side = actions

    children = [left_col]
    if right_side is not None:
        children.append(right_side)

    final_style = _DEFAULT_HEADER_STYLE.merge(style)

    return _Row(
        *children,
        style=final_style,
        **props,
    )
