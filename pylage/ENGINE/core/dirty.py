from __future__ import annotations

import threading
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.graph import DependencyGraph
from pylage.ENGINE.core.state import State


class DirtyNodes:
    """Tracks components invalidated by reactive state changes."""

    def __init__(self) -> None:
        self._nodes: set[Component] = set()
        self._ordered_nodes: list[Component] = []
        self._changed_props: dict[Component, set[str]] = {}
        self._flushing_props: dict[Component, set[str]] = {}
        self._lock = threading.Lock()

    def mark(
        self,
        component: Component,
        prop_name: str | None = None,
    ) -> None:
        with self._lock:
            if component not in self._nodes:
                self._nodes.add(component)
                self._ordered_nodes.append(component)

            if prop_name is not None:
                self._changed_props.setdefault(component, set()).add(
                    prop_name
                )

    def changed_props(self, component: Component) -> set[str] | None:
        """Return changed prop names for a dirty component."""
        with self._lock:
            props = self._flushing_props.get(component)

            if props is not None:
                return set(props)

            props = self._changed_props.get(component)

            if props is None:
                return None

            return set(props)

    def nodes(self) -> list[Component]:
        """Return dirty components in deterministic insertion order."""
        with self._lock:
            return list(self._ordered_nodes)

    def begin_flush(self) -> list[Component]:
        """Snapshot changed props and clear the active dirty batch.

        The snapshot remains available through ``changed_props()`` while
        scheduler callbacks are executing. New reactive changes are tracked
        independently for the next batch.
        """
        with self._lock:
            self._flushing_props = {
                component: set(props)
                for component, props in self._changed_props.items()
            }

            nodes = list(self._ordered_nodes)

            self._nodes.clear()
            self._ordered_nodes.clear()
            self._changed_props.clear()

            return nodes

    def end_flush(self) -> None:
        """Discard the completed flush snapshot."""
        with self._lock:
            self._flushing_props.clear()

    def drain(self) -> list[tuple[Component, set[str] | None]]:
        """Atomically take the current dirty batch and clear it.

        The returned prop metadata belongs to this exact batch and therefore
        remains available while callbacks execute.
        """
        with self._lock:
            batch = [
                (
                    component,
                    (
                        set(self._changed_props[component])
                        if component in self._changed_props
                        else None
                    ),
                )
                for component in self._ordered_nodes
            ]

            self._nodes.clear()
            self._ordered_nodes.clear()
            self._changed_props.clear()

            return batch

    def mark_from_state(
        self,
        state: State,
        graph: DependencyGraph,
    ) -> None:
        for component, prop_name in graph.get_dependents(state):
            self.mark(component, prop_name)

    def contains(self, component: Component) -> bool:
        with self._lock:
            return component in self._nodes

    def clear(self) -> None:
        with self._lock:
            self._nodes.clear()
            self._ordered_nodes.clear()
            self._changed_props.clear()

    def __len__(self) -> int:
        with self._lock:
            return len(self._nodes)
