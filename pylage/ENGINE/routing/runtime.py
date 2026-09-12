from __future__ import annotations

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.routing.router import Router


class RoutingRuntime:
    """Resolve routes and swap the stable root's children on navigation."""

    def __init__(self, router: Router, root: Component) -> None:
        if not isinstance(root, Component):
            raise TypeError("RoutingRuntime expects a Component root.")
        self._router = router
        self._root = root
        self._current_path: str | None = None

    @property
    def current_path(self) -> str | None:
        return self._current_path

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

        self._set_root_children([component])
        self._current_path = normalized
        return component

    def _set_root_children(self, children: list[Component]) -> None:
        root = self._root
        if hasattr(root, "set_children") and callable(root.set_children):
            # Component.set_children takes *children, not a nested list.
            root.set_children(*children)
            return
        if hasattr(root, "children"):
            try:
                root.children = list(children)
                return
            except Exception:
                pass
        raise RuntimeError(
            "RoutingRuntime root does not support set_children/children assignment."
        )
