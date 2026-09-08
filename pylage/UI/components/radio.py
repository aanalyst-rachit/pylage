from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import RadioGroup as _RadioGroup
from pylage.ENGINE.styling.style import Style


_BASE_STYLE = Style(
    display="flex",
    flex_direction="column",
    gap="0.5rem",
)


def radio_group(
    *children: Any,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI Kit radio group using the existing engine RadioGroup."""
    return _RadioGroup(
        *children,
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["radio_group"]
