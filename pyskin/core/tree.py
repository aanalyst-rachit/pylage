from __future__ import annotations

from typing import Any

from .component import Component


def print_tree(node: Any, depth: int = 0) -> None:
    indent = "  " * depth

    if isinstance(node, Component):
        print(f"{indent}{node.type} [{node.id}]")

        if node.props:
            print(f"{indent}  props={node.props}")

        for child in node.children:
            print_tree(child, depth + 1)

    else:
        print(f"{indent}{node!r}")


def collect_ids(node: Any) -> list[str]:
    if not isinstance(node, Component):
        return []

    ids = [node.id]

    for child in node.children:
        ids.extend(collect_ids(child))

    return ids


def count_components(node: Any) -> int:
    if not isinstance(node, Component):
        return 0

    return 1 + sum(
        count_components(child)
        for child in node.children
    )

class TreeMutationObserver:
    """Observe mutations anywhere inside a Component tree."""

    def __init__(
        self,
        root: Component,
        callback,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "TreeMutationObserver expects a Component root."
            )

        if not callable(callback):
            raise TypeError(
                "TreeMutationObserver callback must be callable."
            )

        self.root = root
        self.callback = callback
        self._subscriptions = []

        self._bind_tree(root)

    def _bind_tree(self, node: Any) -> None:
        if not isinstance(node, Component):
            return

        unsubscribe = node.subscribe_mutation(
            self._on_mutation
        )

        self._subscriptions.append(unsubscribe)

        for child in node.children:
            self._bind_tree(child)

    def _on_mutation(self, event: dict[str, Any]) -> None:
        for child in event.get("children", []):
            self._bind_tree(child)

        self.callback(event)

    def stop(self) -> None:
        """Remove all mutation subscriptions."""

        for unsubscribe in self._subscriptions:
            unsubscribe()

        self._subscriptions.clear()

