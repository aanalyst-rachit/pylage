from typing import Any

from pylage.ENGINE.components.basic import Row, Button
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.styling.style import Style


def navigation_controls(
    on_prev: Any = None,
    on_next: Any = None,
    style: Style | None = None,
    **props: Any,
) -> Component:
    base_style = Style(display="flex", gap="0.5rem", align_items="center")
    prev_btn = Button("Previous", on_click=on_prev) if on_prev else Button("Previous")
    next_btn = Button("Next", on_click=on_next) if on_next else Button("Next")
    return Row(prev_btn, next_btn, style=base_style.merge(style), **props)


# Backward-compatible CamelCase alias.
NavigationControls = navigation_controls


__all__ = ["navigation_controls", "NavigationControls"]
