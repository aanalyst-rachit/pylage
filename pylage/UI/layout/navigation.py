from typing import Any

from pylage.ENGINE.components.basic import Navigation as _Navigation
from pylage.ENGINE.core.component import Component


def navigation(*children: Any, **props: Any) -> Component:
    return _Navigation(*children, **props)


# Backward-compatible CamelCase alias.
Navigation = navigation


__all__ = ["navigation", "Navigation"]
