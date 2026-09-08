from __future__ import annotations

from typing import Any, Callable

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.registry import registry
from pylage.ENGINE.core.state import State
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.dirty import DirtyNodes
from pylage.ENGINE.core.scheduler import Scheduler
from pylage.ENGINE.styling.style import Style


UpdateCallback = Callable[[Component, dict[str, Any]], None]


class StateBinding:
    """Binds reactive State values inside a component tree."""

    def __init__(
        self,
        root: Component,
        callback: UpdateCallback,
        graph: DependencyGraph | None = None,
        dirty: DirtyNodes | None = None,
        scheduler: Scheduler | None = None,
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
        self.graph = graph
        self.dirty = dirty
        self.scheduler = scheduler
        self._subscriptions: list[Callable[[], None]] = []
        self._node_bindings: dict[str, list[tuple[State, Component, str, Callable[[], None]]]] = {}

        self.bind_tree(root)

    def _is_reactive(
        self,
        component: Component,
        prop_name: str,
    ) -> bool:
        """Return whether a component prop participates in reactivity."""

        definition = registry.get(component.type)

        if definition is None or definition.props is None:
            # Preserve backward compatibility for unknown components
            # and props that have no registry contract.
            return True

        prop_definition = definition.props.get(prop_name)

        if prop_definition is None:
            # Preserve existing behavior for unknown props.
            return True

        return prop_definition.reactive

    def _iter_states(self, value: Any):
        """Yield reactive State objects nested inside supported values."""
        if isinstance(value, State):
            yield value
            return

        if isinstance(value, Style):
            for field_name in value.__dataclass_fields__:
                field_value = getattr(value, field_name)
                if isinstance(field_value, State):
                    yield field_value
            for field_value in (value.custom or {}).values():
                if isinstance(field_value, State):
                    yield field_value

    def _bind_single_node(self, node: Component) -> None:
        if node.id in self._node_bindings:
            # Already bound; unbind first to avoid duplicate subscriptions
            self._unbind_single_node(node)

        node_records: list[tuple[State, Component, str, Callable[[], None]]] = []

        for prop_name, value in node.props.items():
            if not self._is_reactive(node, prop_name):
                continue

            for state in self._iter_states(value):
                unsubscribe = state.subscribe(
                    lambda old, new,
                    component=node,
                    name=prop_name: self._changed(
                        component,
                        name,
                        new,
                    )
                )

                node_records.append((state, node, prop_name, unsubscribe))
                self._subscriptions.append(unsubscribe)

                if self.graph is not None:
                    self.graph.add_dependency(
                        state,
                        node,
                        prop_name,
                    )

        self._node_bindings[node.id] = node_records

    def _unbind_single_node(self, node: Component) -> None:
        records = self._node_bindings.pop(node.id, [])
        for value, comp, prop_name, unsubscribe in records:
            try:
                unsubscribe()
            except Exception:
                pass
            if unsubscribe in self._subscriptions:
                self._subscriptions.remove(unsubscribe)
            if self.graph is not None:
                self.graph.remove_dependency(value, comp, prop_name)

    def bind_tree(self, node: Any) -> None:
        """Recursively bind a component and all its children."""
        if not isinstance(node, Component):
            return

        self._bind_single_node(node)

        for child in node.children:
            self.bind_tree(child)

    def bind(self, node: Any) -> None:
        """Bind a newly-added component or subtree to state updates."""
        self.bind_tree(node)

    def unbind_tree(self, node: Any) -> None:
        """Recursively unbind a component and all its children from state updates."""
        if not isinstance(node, Component):
            return

        self._unbind_single_node(node)

        for child in node.children:
            self.unbind_tree(child)

    def unbind(self, node: Any) -> None:
        """Unbind a component or subtree from state updates."""
        self.unbind_tree(node)

    def _changed(
        self,
        component: Component,
        prop_name: str,
        value: Any,
    ) -> None:
        # Scheduler mode only marks the component dirty.
        # The scheduler is flushed explicitly at the batching boundary.
        if self.scheduler is not None:
            if self.dirty is not None:
                self.dirty.mark(component, prop_name)

            self.scheduler.request()
            return

        # Preserve the existing immediate callback contract when
        # no scheduler is configured.
        self.callback(
            component,
            {
                prop_name: value,
            },
        )

        if self.dirty is not None:
            self.dirty.mark(component, prop_name)

    def stop(self) -> None:
        """Remove all State subscriptions."""
        for records in list(self._node_bindings.values()):
            for value, comp, prop_name, unsubscribe in records:
                try:
                    unsubscribe()
                except Exception:
                    pass
        self._node_bindings.clear()

        for unsubscribe in self._subscriptions:
            try:
                unsubscribe()
            except Exception:
                pass

        self._subscriptions.clear()

        if self.graph is not None:
            self.graph.clear()
