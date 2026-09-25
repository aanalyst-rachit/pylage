from __future__ import annotations

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State
from pylage.ENGINE.routing.router import Router
from pylage.ENGINE.runtime.logger import log_event


class RoutingRuntime:
    """Resolve routes and swap the stable root's children on navigation."""

    def __init__(
        self,
        router: Router,
        root: Component,
        content_root: Component | None = None,
    ) -> None:
        if not isinstance(root, Component):
            raise TypeError("RoutingRuntime expects a Component root.")
        if content_root is not None and not isinstance(content_root, Component):
            raise TypeError("RoutingRuntime expects a Component content_root.")
        self._router = router
        self._root = root
        self._content_root = content_root
        self._current_path: str | None = None
        self._current_route = None
        self._current_route_state = State(None)
        self._current_path_state = State(None)

    @property
    def current_path(self) -> str | None:
        return self._current_path

    @property
    def current_path_state(self) -> State:
        return self._current_path_state

    @property
    def current_route(self):
        return self._current_route

    @property
    def current_route_state(self) -> State:
        return self._current_route_state

    def navigate(self, path: str) -> Component:
        normalized = path or "/"
        if not normalized.startswith("/"):
            normalized = "/" + normalized
        if len(normalized) > 1:
            normalized = normalized.rstrip("/")

        resolved = self._router.resolve(normalized)
        if resolved is None:
            raise LookupError(f"No route matches path: {normalized}")

        if isinstance(resolved, tuple):
            route, params = resolved
        else:
            route = resolved
            params = {}

        page = self._router.load_page(route)
        page_result = page(**params)
        component = self._router.validate_page_result(page_result, route)

        self._set_route_children([component])
        self._current_route = route
        self._current_route_state.set(route)
        self._current_path = normalized
        self._current_path_state.set(normalized)
        return component

    def _set_route_children(self, children: list[Component]) -> None:
        target = self._content_root or self._root
        if hasattr(target, "set_children") and callable(target.set_children):
            # Component.set_children takes *children, not a nested list.
            target.set_children(*children)
            return
        if hasattr(target, "children"):
            try:
                target.children = list(children)
                return
            except Exception as exc:  # noqa: BLE001 - fallback assignment must isolate arbitrary setter failures
                log_event(30, "routing.target_assignment_error", error=exc)
        raise RuntimeError(
            "RoutingRuntime route target does not support set_children/children assignment."
        )
