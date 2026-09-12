from __future__ import annotations

from typing import Any, Callable

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.reactive_list import ReactiveList


class For(Component):
    """Render one component for each item in a reactive list."""

    def __init__(
        self,
        items: ReactiveList,
        render_item: Callable[[Any], Component],
    ) -> None:
        if not isinstance(items, ReactiveList):
            raise TypeError("items must be a ReactiveList instance")
        if not callable(render_item):
            raise TypeError("render_item must be callable")

        self._items = items
        self._render_item = render_item
        self._items_unsubscribe = None
        self._disposed = False
        self._rendered_items: list[Component] = []

        initial_children = self._render_all(items.value)
        super().__init__(
            type="for",
            children=initial_children,
        )
        self._rendered_items = list(initial_children)
        self._items_unsubscribe = items.subscribe(self._items_changed)

    def _render_one(self, item: Any) -> Component:
        component = self._render_item(item)
        if not isinstance(component, Component):
            raise TypeError("render_item must return a Component")
        return component

    def _render_all(self, items: list[Any]) -> list[Component]:
        return [self._render_one(item) for item in items]

    def _items_changed(self, delta: dict[str, Any]) -> None:
        if self._disposed:
            return

        delta_type = delta.get("type")

        if delta_type == "append":
            rendered = self._render_one(delta["value"])
            self._rendered_items.append(rendered)

        elif delta_type == "insert":
            rendered = self._render_one(delta["value"])
            self._rendered_items.insert(delta["index"], rendered)

        elif delta_type == "remove":
            self._rendered_items.pop(delta["index"])

        elif delta_type == "move":
            rendered = self._rendered_items.pop(delta["from_index"])
            self._rendered_items.insert(delta["to_index"], rendered)

        elif delta_type == "update":
            rendered = self._render_one(delta["value"])
            self._rendered_items[delta["index"]] = rendered

        else:
            raise ValueError(f"Unsupported ReactiveList delta type: {delta_type!r}")

        self.set_children(*self._rendered_items)

    def dispose(self) -> None:
        """Stop reacting to future ReactiveList mutations."""
        if self._disposed:
            return

        if self._items_unsubscribe is not None:
            self._items_unsubscribe()
            self._items_unsubscribe = None

        self._disposed = True


def for_each(
    items: ReactiveList,
    render_item: Callable[[Any], Component],
) -> For:
    """Create a reactive component list from a ReactiveList."""
    return For(items, render_item)


__all__ = ["For", "for_each"]
