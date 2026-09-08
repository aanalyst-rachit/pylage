from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Badge as _Badge
from pylage.ENGINE.styling.style import Style
from pylage.ENGINE.components.basic import Text as _Text
from pylage.ENGINE.core.component import Component


_DIRECTION_CONFIG: dict[str, tuple[str, str]] = {
    "up": ("↑", "success"),
    "down": ("↓", "danger"),
    "neutral": ("→", "secondary"),
}

_VARIANT_STYLES: dict[str, Style] = {
    "success": Style(
        background_color="var(--color-success)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-success)",
    ),
    "danger": Style(
        background_color="var(--color-danger)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-danger)",
    ),
    "secondary": Style(
        background_color="var(--color-secondary)",
        color="var(--color-secondary-contrast)",
        border="1px solid var(--color-secondary)",
    ),
}

_BASE_STYLE = Style(
    padding="0.25rem 0.625rem",
    border_radius="var(--radius-full)",
    font_size="0.75rem",
    font_weight="600",
)


def _detect_direction(value: Any) -> str:
    resolved = str(getattr(value, "value", value))

    if resolved.startswith("+"):
        return "up"

    if resolved.startswith("-"):
        return "down"

    return "neutral"


def trend(
    value: Any,
    *,
    direction: str | None = None,
    show_indicator: bool = True,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit trend indicator.

    Direction is automatically detected from leading ``+`` or ``-`` signs
    unless explicitly provided.
    """
    final_direction = direction or _detect_direction(value)

    if final_direction not in _DIRECTION_CONFIG:
        valid = ", ".join(_DIRECTION_CONFIG)
        raise ValueError(
            f"Unknown trend direction {final_direction!r}. "
            f"Expected one of: {valid}."
        )

    indicator, variant = _DIRECTION_CONFIG[final_direction]

    default_style = _BASE_STYLE.merge(_VARIANT_STYLES[variant])
    final_style = default_style.merge(style)

    children = []

    if show_indicator:
        children.append(_Text(indicator))

    children.append(
        value if isinstance(value, Component) else _Text(value)
    )

    return _Badge(
        *children,
        style=final_style,
        **props,
    )
