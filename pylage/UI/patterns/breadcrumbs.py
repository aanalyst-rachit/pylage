"""Breadcrumb pattern for PyLage UI."""

from typing import Any

from pylage.ENGINE.components import Breadcrumbs as _Breadcrumbs
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State


def breadcrumb_trail(
    *children: Any,
    class_name: str | None = None,
    current_path: str | State | None = None,
    current_route: Any | State | None = None,
    **props: Any,
) -> Component:
    if class_name is not None:
        props["class_name"] = class_name

    if current_path is None and current_route is None:
        return _Breadcrumbs(*children, **props)

    component = _Breadcrumbs(**props)

    def build_items(
        path: str | None,
        route: Any = None,
    ) -> list[Component]:
        normalized = path or "/"

        if not normalized.startswith("/"):
            normalized = "/" + normalized

        if len(normalized) > 1:
            normalized = normalized.rstrip("/")

        if normalized == "/":
            return [
                Component(
                    type="Text",
                    props={"text": "Home"},
                )
            ]

        segments = [
            segment
            for segment in normalized.strip("/").split("/")
            if segment
        ]

        items: list[Component] = [
            Component(
                type="Link",
                props={
                    "text": "Home",
                    "href": "/",
                },
            )
        ]

        accumulated = ""

        for index, segment in enumerate(segments):
            accumulated += f"/{segment}"
            label = segment.replace("-", " ").replace("_", " ").title()

            if index == len(segments) - 1:
                route_label = getattr(route, "label", None)
                if isinstance(route_label, str) and route_label:
                    label = route_label

                items.append(
                    Component(
                        type="Text",
                        props={"text": label},
                    )
                )
            else:
                items.append(
                    Component(
                        type="Link",
                        props={
                            "text": label,
                            "href": accumulated,
                        },
                    )
                )

        return items

    path_value = (
        current_path.value
        if isinstance(current_path, State)
        else current_path
    )
    route_value = (
        current_route.value
        if isinstance(current_route, State)
        else current_route
    )

    component.set_children(*build_items(path_value, route_value))

    def update_path(_old: Any, new: Any) -> None:
        route = (
            current_route.value
            if isinstance(current_route, State)
            else current_route
        )
        component.set_children(*build_items(new, route))

    def update_route(_old: Any, new: Any) -> None:
        path = (
            current_path.value
            if isinstance(current_path, State)
            else current_path
        )
        component.set_children(*build_items(path, new))

    if isinstance(current_path, State):
        unsubscribe = current_path.subscribe(update_path)
        component.add_cleanup(unsubscribe)

    if isinstance(current_route, State):
        unsubscribe = current_route.subscribe(update_route)
        component.add_cleanup(unsubscribe)

    return component


# Backward-compatible CamelCase alias.
BreadcrumbTrail = breadcrumb_trail


__all__ = ["BreadcrumbTrail", "breadcrumb_trail"]
