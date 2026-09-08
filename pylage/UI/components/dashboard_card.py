from __future__ import annotations

from typing import Any
from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.components.basic import Heading as _Heading
from pylage.ENGINE.components.basic import Row as _Row
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Text as _Text
from .card import card as _card

_TITLE_STYLE = Style(
    font_size="1.125rem",
    font_weight="600",
    color="var(--color-text)",
    margin="0",
)

def dashboard_card(
    *children: Any,
    title: Any = None,
    body: Any = None,
    footer: Any = None,
    action: Any = None,
    variant: str = "elevated",
    style: Style | None = None,
    **props: Any,
):
    """Create a high-level card designed for dashboard widgets."""
    content: list[Any] = []

    if title is not None or action is not None:
        title_comp = title if hasattr(title, "type") else _Heading(title, level=3, style=_TITLE_STYLE) if title else None
        top_items = []
        if title_comp:
            top_items.append(title_comp)
        if action:
            top_items.append(action)

        if len(top_items) == 1 and not action:
            content.append(top_items[0])
        else:
            top_row = _Row(
                *top_items,
                style=Style(
                    display="flex",
                    flex_direction="row",
                    justify_content="space-between",
                    align_items="center",
                    width="100%",
                    margin_bottom="var(--spacing-sm)",
                ),
            )
            content.append(top_row)

    if body is not None:
        content.append(_Text(body) if isinstance(body, str) else body)

    content.extend(children)

    if footer is not None:
        content.append(_Text(footer, style=Style(font_size="0.75rem", color="var(--color-text-muted)")) if isinstance(footer, str) else footer)

    return _card(
        *content,
        variant=variant,
        style=style,
        **props,
    )
