from __future__ import annotations

from typing import Any, Callable

from pyskin.core.component import Component
from pyskin.core.state import State


UpdateCallback = Callable[[Component, dict[str, Any]], None]


class StateBinding:
    """Binds State values inside a component to update callbacks."""

    def __init__(
        self,
        root: Component,
        callback: UpdateCallback,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError(
                "StateBinding expects a Component root."
            )

        if not callable(callback):
            raise TypeError(
                "StateBinding callback must be callable."
            )

        self.root = root
        self.callback = callback
        self._subscriptions: list[Callable[[], None]] = []

        self._bind_tree(root)

    def _bind_tree(self, node: Any) -> None:
        if not isinstance(node, Component):
            return

        for prop_name, value in node.props.items():
            if isinstance(value, State):
                unsubscribe = value.subscribe(
                    lambda old, new,
                    component=node,
                    name=prop_name: self._changed(
                        component,
                        name,
                        new,
                    )
                )

                self._subscriptions.append(unsubscribe)

        for child in node.children:
            self._bind_tree(child)

    def _changed(
        self,
        component: Component,
        prop_name: str,
        value: Any,
    ) -> None:
        self.callback(
            component,
            {
                prop_name: value,
            },
        )

    def stop(self) -> None:
        """Remove all State subscriptions."""

        for unsubscribe in self._subscriptions:
            unsubscribe()

        self._subscriptions.clear()
