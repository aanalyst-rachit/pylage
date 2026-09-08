from typing import Any

from pylage.ENGINE.components.basic import Pagination as _Pagination
from pylage.ENGINE.core.component import Component


def pagination(*children: Any, **props: Any) -> Component:
    return _Pagination(*children, **props)


# Backward-compatible CamelCase alias.
Pagination = pagination


__all__ = ["pagination", "Pagination"]
