from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Switch as _Switch
from pylage.ENGINE.styling.style import Style


_BASE_STYLE = Style(
    width="2.75rem",
    height="1.5rem",
    cursor="pointer",
)


def switch(
    *,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI switch using the existing engine Switch."""
    return _Switch(
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["switch"]
