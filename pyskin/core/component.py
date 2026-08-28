from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable
import uuid


Child = Any
EventHandler = Callable[..., Any]


@dataclass
class Component:
    type: str
    props: dict[str, Any] = field(default_factory=dict)
    children: list[Child] = field(default_factory=list)
    events: dict[str, EventHandler] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])

    def add(self, *children: Child) -> "Component":
        self.children.extend(children)
        return self

    def on(
        self,
        event: str,
        handler: EventHandler,
    ) -> "Component":
        if not isinstance(event, str) or not event:
            raise ValueError("event must be a non-empty string")

        if not callable(handler):
            raise TypeError("handler must be callable")

        self.events[event] = handler
        return self

    def __repr__(self) -> str:
        return (
            f"Component("
            f"type={self.type!r}, "
            f"id={self.id!r}, "
            f"props={self.props!r}, "
            f"children={self.children!r}, "
            f"events={list(self.events)!r})"
        )


def component(
    type: str,
    *children: Child,
    **props: Any,
) -> Component:
    normalized_children = [
        child for child in children
        if child is not None
    ]

    events: dict[str, EventHandler] = {}

    event_props = {
        key: value
        for key, value in props.items()
        if key.startswith("on_")
    }

    for key in event_props:
        props.pop(key)

    for key, handler in event_props.items():
        event_name = key[3:]

        if not callable(handler):
            raise TypeError(
                f"{key} must be callable"
            )

        events[event_name] = handler

    return Component(
        type=type,
        props=dict(props),
        children=normalized_children,
        events=events,
    )
