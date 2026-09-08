from __future__ import annotations

from typing import Any, Callable

from pylage.ENGINE.components.basic import Button as _Button
from pylage.ENGINE.core.state import State
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
    style: Style | None = None,
    **props: Any,
) -> Any:
    """Create a semantic navigation item using the existing PyLage Button.

    active may be a boolean for static usage or a State for
    controlled reactive navigation.
    """
    if isinstance(active, State):
        final_style, update_active = _resolve_reactive_style(active, style)
        component = _Button(
            text,
            style=final_style,
            **props,
        )
        active.subscribe(update_active)
        return component

    if not isinstance(active, bool):
        raise TypeError("active must be a bool or State")

    return _Button(
        text,
        style=_resolve_style(active, style),
        **props,
    )


__all__ = ["navigation_item"]
