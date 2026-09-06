from __future__ import annotations

from typing import Any

from pylage.ENGINE import Heading as _Heading
from pylage.ENGINE import Style


_BASE_STYLE = Style(
    margin="0",
    color="var(--color-text)",
    font_weight="700",
    line_height="1.25",
)


def heading(
    value: Any,
    *,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit heading using the existing PyLage Heading."""

    return _Heading(
        value,
        style=_BASE_STYLE.merge(style),
        **props,
    )
