from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Card as _Card
from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.components.basic import Heading as _Heading
from pylage.ENGINE.components.basic import Text as _Text



_DEFAULT_CARD_STYLE = Style(
    display="flex",
    flex_direction="column",
    gap="var(--spacing-sm)",
    padding="var(--spacing-lg)",
    background_color="var(--color-background)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-xl)",
)


_LABEL_STYLE = Style(
    font_size="0.875rem",
    font_weight="500",
    color="var(--color-text-muted)",
    margin="0",
)


_VALUE_STYLE = Style(
    font_size="1.75rem",
    font_weight="700",
    color="var(--color-text)",
    margin="0",
)


_DELTA_STYLE = Style(
    font_size="0.875rem",
    font_weight="600",
    color="var(--color-success)",
    margin="0",
)


_DESCRIPTION_STYLE = Style(
    font_size="0.75rem",
    color="var(--color-text-muted)",
    margin="0",
)


def metric(
    label: Any,
    value: Any,
    delta: Any = None,
    description: Any = None,
    *,
    featured: bool = False,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic KPI/metric card using only PyLage engine primitives."""

    items: list[Any] = []

    if label is not None:
        items.append(_Text(label, style=_LABEL_STYLE))

    if value is not None:
        items.append(_Heading(value, level=2, style=_VALUE_STYLE))

    if delta is not None:
        items.append(_Text(delta, style=_DELTA_STYLE))

    if description is not None:
        items.append(_Text(description, style=_DESCRIPTION_STYLE))

    card_style = _DEFAULT_CARD_STYLE

    if featured:
        card_style = card_style.merge(
            Style(
                border="2px solid var(--color-primary)",
            )
        )

    final_style = card_style.merge(style)

    return _Card(
        _Column(
            *items,
            style=Style(
                display="flex",
                flex_direction="column",
                gap="var(--spacing-sm)",
            ),
        ),
        style=final_style,
        **props,
    )
