from __future__ import annotations

from pathlib import Path
from typing import Any

from pylage.ENGINE.routing import Router, RoutingRuntime
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State
from pylage.UI.components.navigation_item import navigation_item


class App:
    def __init__(
        self,
        *,
        pages: str | Path | None = None,
        navigation: Component | None = None,
        **kwargs: Any,
    ):
        self.pages = Path(pages) if pages is not None else None
        self.navigation = navigation
        self.kwargs = kwargs

        self.router = Router(self.pages) if self.pages else None
        self.content = Component()
        self.routing = (
            RoutingRuntime(self.router, self.content)
            if self.router
            else None
        )

    def navigate(self, path: str) -> None:
        if self.routing:
            self.routing.navigate(path)

    def render(self) -> Component:
        if self.routing:
            self.routing.navigate("/")
        return self.content
