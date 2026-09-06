from __future__ import annotations

from typing import Any

from pylage.ENGINE import Slider as _Slider
from pylage.ENGINE import Style


_BASE_STYLE = Style(
    width="100%",
    cursor="pointer",
)


def slider(
    *,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI slider using the existing engine Slider."""
    return _Slider(
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["slider"]
