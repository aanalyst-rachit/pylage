from __future__ import annotations

from typing import Any

from pyskin.core.component import Component
from pyskin.core.registry import registry


def component_to_snapshot(
    component: Component,
) -> dict[str, Any]:
    """Create a stable, serializable representation of a Component tree."""

    if not isinstance(component, Component):
        raise TypeError(
            "component_to_snapshot expects a Component."
        )

    definition = registry.get(component.type)

    return {
        "id": component.id,
        "type": component.type,
        "tag": (
            definition.tag
            if definition is not None
            else "div"
        ),
        "events": ",".join(component.events),
        "props": dict(component.props),
        "children": [
            component_to_snapshot(child)
            for child in component.children
            if isinstance(child, Component)
        ],
    }
