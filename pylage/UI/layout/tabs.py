from typing import Any

from pylage.ENGINE.components.basic import Tabs as _Tabs
from pylage.ENGINE.core.component import Component


def tabs(*children: Any, **props: Any) -> Component:
    return _Tabs(*children, **props)


# Backward-compatible CamelCase alias.
Tabs = tabs


__all__ = ["tabs", "Tabs"]
