from __future__ import annotations

from typing import Any

from pylage.ENGINE import Form as _Form
from pylage.ENGINE import Style


_BASE_STYLE = Style(
    display="flex",
    flex_direction="column",
    gap="1rem",
    width="100%",
)


def form(
    *children: Any,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI form using the existing engine Form."""
    return _Form(
        *children,
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["form"]
