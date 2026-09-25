from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pylage.ENGINE.components.basic import Button as _Button
from pylage.ENGINE.components.basic import Link as _Link
from pylage.ENGINE.core.state import DerivedState, State
from pylage.ENGINE.styling.style import Style

_BASE_STYLE = Style(
    display="flex",
    align_items="center",
    width="100%",
    text_align="left",
    background_color="transparent",
    color="var(--color-text)",
    border="none",
    border_radius="0.375rem",
    padding="0.5rem 0.75rem",
    cursor="pointer",
)


_ACTIVE_STYLE = Style(
    background_color="var(--color-primary)",
    color="var(--color-primary-contrast)",
    border="none",
)


def _resolve_style(active: bool, style: Style | None) -> Style:
    default_style = _BASE_STYLE.merge(_ACTIVE_STYLE if active else None)
    return default_style.merge(style)


def _resolve_reactive_style(
    active: State,
    style: Style | None,
) -> tuple[Style, Callable[[Any, Any], None]]:
    custom = style or Style()

    background = State(
        "var(--color-primary)" if bool(active.value) else "transparent"
    )
    color = State(
        "var(--color-primary-contrast)" if bool(active.value) else "var(--color-text)"
    )
    default_style = Style(
        display="flex",
        align_items="center",
        width="100%",
        text_align="left",
        background_color=background,
        color=color,
        border="none",
        border_radius="0.375rem",
        padding="0.5rem 0.75rem",
        cursor="pointer",
    )

    final_style = default_style.merge(custom)

    def update_active(_old: Any, new: Any) -> None:
        if custom.background_color is None:
            background.set(
                "var(--color-primary)" if bool(new) else "transparent"
            )
        if custom.color is None:
            color.set(
                "var(--color-primary-contrast)" if bool(new) else "var(--color-text)"
            )
    return final_style, update_active


def navigation_item(
    text: Any,
    *,
    active: bool | State = False,
    current_path: str | State | None = None,
    style: Style | None = None,
    **props: Any,
) -> Any:
    """Create a navigation item while preserving the legacy button API.

    Route-aware items use Link semantics when ``href`` is provided.
    Route-less items retain the original Button semantics.
    """
    if current_path is not None:
        href = props.get("href")
        if not isinstance(href, str) or not href:
            raise ValueError(
                "current_path requires a non-empty string href"
            )

        if isinstance(current_path, State):
            active = DerivedState(
                current_path,
                compute=lambda path: path == href,
            )
        elif isinstance(current_path, str):
            active = current_path == href
        else:
            raise TypeError("current_path must be a str, State, or None")

    component_factory = _Link if "href" in props else _Button

    if isinstance(active, State):
        final_style, update_active = _resolve_reactive_style(active, style)
        component = component_factory(
            text,
            style=final_style,
            **props,
        )
        active.subscribe(update_active)

        if isinstance(active, DerivedState):
            component.add_cleanup(active.dispose)

        return component

    if not isinstance(active, bool):
        raise TypeError("active must be a bool or State")

    return component_factory(
        text,
        style=_resolve_style(active, style),
        **props,
    )


__all__ = ["navigation_item"]
