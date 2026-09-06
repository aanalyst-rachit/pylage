from __future__ import annotations

from typing import Any

from pylage.ENGINE import Checkbox as _Checkbox
from pylage.ENGINE import Style


_BASE_STYLE = Style(
    width="1rem",
    height="1rem",
    cursor="pointer",
)


def checkbox(
    *,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI checkbox using the existing engine Checkbox."""
    return _Checkbox(
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["checkbox"]
