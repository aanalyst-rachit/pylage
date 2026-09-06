from __future__ import annotations

from typing import Any
from pylage.ENGINE import Column as _Column
from pylage.ENGINE import Heading as _Heading
from pylage.ENGINE import Row as _Row
from pylage.ENGINE import Style
from pylage.ENGINE import Text as _Text

_DEFAULT_SECTION_STYLE = Style(
    display="flex",
    flex_direction="column",
    width="100%",
    gap="var(--spacing-md)",
)

_TITLE_STYLE = Style(
    font_size="1.25rem",
    font_weight="600",
    color="var(--color-text)",
    margin="0",
)

_DESC_STYLE = Style(
    font_size="0.875rem",
    color="var(--color-text-muted)",
    margin="0",
)

def dashboard_section(
    *children: Any,
    title: Any = None,
    description: Any = None,
    action: Any = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a structured dashboard section with header and body content."""
    elements: list[Any] = []

    if title is not None or description is not None or action is not None:
        header_text_items: list[Any] = []
        if title is not None:
            if hasattr(title, "type"):
                header_text_items.append(title)
            else:
                header_text_items.append(_Heading(title, level=2, style=_TITLE_STYLE))

        if description is not None:
            if hasattr(description, "type"):
                header_text_items.append(description)
            else:
                header_text_items.append(_Text(description, style=_DESC_STYLE))

        left_side = _Column(
            *header_text_items,
            style=Style(display="flex", flex_direction="column", gap="0.125rem"),
        )

        header_row_items = [left_side]
        if action is not None:
            header_row_items.append(action)

        header_row = _Row(
            *header_row_items,
            style=Style(
                display="flex",
                flex_direction="row",
                justify_content="space-between",
                align_items="center",
                width="100%",
            ),
        )
        elements.append(header_row)

    elements.extend(children)

    final_style = _DEFAULT_SECTION_STYLE.merge(style)

    return _Column(
        *elements,
        style=final_style,
        **props,
    )
