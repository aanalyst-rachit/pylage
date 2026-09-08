from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Text as _Text


_MUTED_STYLE = Style(
    color="var(--color-text-muted)",
)

_LABEL_STYLE = Style(
    color="var(--color-text)",
    font_size="0.875rem",
    font_weight="500",
)

_CAPTION_STYLE = Style(
    color="var(--color-text-muted)",
    font_size="0.75rem",
)


def text(
    value: Any,
    *,
    muted: bool = False,
    label: bool = False,
    caption: bool = False,
    style: Style | None = None,
    **props: Any,
):
    """Create semantic UI Kit text using the existing PyLage Text."""

    default_style = Style()

    if muted:
        default_style = default_style.merge(_MUTED_STYLE)

    if label:
        default_style = default_style.merge(_LABEL_STYLE)

    if caption:
        default_style = default_style.merge(_CAPTION_STYLE)

    final_style = default_style.merge(style)

    return _Text(
        value,
        style=final_style,
        **props,
    )
