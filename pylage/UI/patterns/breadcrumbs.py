"""Breadcrumb pattern for PyLage UI."""

from typing import Any

from pylage.ENGINE.components import Breadcrumbs as _Breadcrumbs
from pylage.ENGINE.core.component import Component


def breadcrumb_trail(
    *children: Any,
    class_name: str | None = None,
    **props: Any,
) -> Component:
    if class_name is not None:
        props["class_name"] = class_name

    return _Breadcrumbs(*children, **props)


# Backward-compatible CamelCase alias.
BreadcrumbTrail = breadcrumb_trail


__all__ = ["breadcrumb_trail", "BreadcrumbTrail"]
