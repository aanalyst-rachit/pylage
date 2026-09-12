from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import importlib.util
import re

from pylage.ENGINE.core.component import Component


@dataclass(frozen=True)
class Route:
    path: str
    source: Path


class Router:
    """Build an in-memory route table from a pages directory."""

    def __init__(self, pages_dir: str | Path):
        self.pages_dir = Path(pages_dir).resolve()

        if not self.pages_dir.is_dir():
            raise ValueError(
                f"PyLage pages directory does not exist: {pages_dir}"
            )

        self._routes = self._scan()
        self._pages = self._load_pages()

    def _scan(self) -> tuple[Route, ...]:
        routes: list[Route] = []

        for source in sorted(self.pages_dir.rglob("*.py")):
            if source.name.startswith("_"):
                continue

            relative = source.relative_to(self.pages_dir)
            route = self._route_from_path(relative)
            routes.append(Route(route, source))

        routes.sort(key=lambda item: (len(self._route_parameters(item.path)), item.path))
        return tuple(routes)

    @staticmethod
    def _route_from_path(relative: Path) -> str:
        parts = list(relative.parts)

        if parts[-1] == "index.py":
            parts.pop()
        else:
            parts[-1] = relative.stem

        if not parts:
            return "/"

        converted: list[str] = []
        for part in parts:
            match = re.fullmatch(r"\[([A-Za-z_][A-Za-z0-9_]*)\]", part)
            if match:
                converted.append(f":{match.group(1)}")
            else:
                converted.append(part)

        return "/" + "/".join(converted)

    def _load_pages(self) -> dict[Path, object]:
        pages: dict[Path, object] = {}
        for route in self._routes:
            pages[route.source] = self._load_page(route)
        return pages

    @staticmethod
    def _route_parameters(path: str) -> tuple[str, ...]:
        return tuple(re.findall(r":([A-Za-z_][A-Za-z0-9_]*)", path))

    @property
    def routes(self) -> tuple[Route, ...]:
        return self._routes

    def _load_page(self, route: Route) -> object:
        """Import and validate one page module."""
        module_name = f"_pylage_page_{abs(hash(route.source))}"
        spec = importlib.util.spec_from_file_location(module_name, route.source)

        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load page module: {route.source}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

    def load_page(self, route: Route) -> object:
        """Return and validate the cached page handler for a route."""
        if route not in self._routes:
            raise ValueError("Route does not belong to this Router.")

        module = self._pages[route.source]
        page = getattr(module, "page", None)

        if page is None:
            raise TypeError(
                f"Page module {route.source} must define page(...)."
            )

        if not callable(page):
            raise TypeError(
                f"Page module {route.source} page must be callable."
            )

        return page

    @staticmethod
    def validate_page_result(page_result: object, route: Route) -> Component:
        """Validate that a rendered page returns a Component."""
        if not isinstance(page_result, Component):
            raise TypeError(
                f"Page {route.path} must return a Component."
            )

        return page_result

    def resolve(self, path: str) -> Route | tuple[Route, dict[str, str]] | None:
        normalized = path or "/"

        if not normalized.startswith("/"):
            normalized = "/" + normalized

        if len(normalized) > 1:
            normalized = normalized.rstrip("/")

        for route in self._routes:
            route_parts = (
                []
                if route.path == "/"
                else route.path.strip("/").split("/")
            )
            path_parts = (
                []
                if normalized == "/"
                else normalized.strip("/").split("/")
            )

            if len(route_parts) != len(path_parts):
                continue

            params: dict[str, str] = {}
            matched = True

            for route_part, path_part in zip(route_parts, path_parts):
                if route_part.startswith(":"):
                    params[route_part[1:]] = path_part
                elif route_part != path_part:
                    matched = False
                    break

            if matched:
                if self._route_parameters(route.path):
                    return route, params
                return route

        return None
