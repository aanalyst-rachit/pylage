from typing import Any

from pylage.ENGINE.components.basic import Menu as _Menu
from pylage.ENGINE.core.component import Component


def menu(*children: Any, **props: Any) -> Component:
    return _Menu(*children, **props)


# Backward-compatible CamelCase alias.
Menu = menu


__all__ = ["menu", "Menu"]
