from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.responsive import ResponsiveStyle
from pylage.ENGINE.styling.style import Style


SPACING_PROPS = {
    "p": ("padding",),
    "px": ("padding_left", "padding_right"),
    "py": ("padding_top", "padding_bottom"),
    "pt": ("padding_top",),
    "pr": ("padding_right",),
    "pb": ("padding_bottom",),
    "pl": ("padding_left",),
    "m": ("margin",),
    "mx": ("margin_left", "margin_right"),
    "my": ("margin_top", "margin_bottom"),
    "mt": ("margin_top",),
    "mr": ("margin_right",),
    "mb": ("margin_bottom",),
    "ml": ("margin_left",),
    "gap": ("gap",),
    "row_gap": ("row_gap",),
    "column_gap": ("column_gap",),
}


def _resolve_spacing(value: Any) -> Any:
    if isinstance(value, str) and value in {"xs", "sm", "md", "lg", "xl"}:
        return "var(--spacing-" + value + ")"
    return value

def spacing_style(props: dict[str, Any]) -> Style:
    values: dict[str, Any] = {}

    for shorthand, fields in SPACING_PROPS.items():
        if shorthand not in props:
            continue
        value = _resolve_spacing(props.pop(shorthand))
        for field in fields:
            values[field] = value

    return Style(**values)


def responsive_style(value: dict[str, dict[str, Any]]) -> ResponsiveStyle:
    styles: dict[str, Style | None] = {}

    for breakpoint in ("base", "sm", "md", "lg", "xl"):
        mapping = value.get(breakpoint)
        if mapping is None:
            styles[breakpoint] = None
            continue

        resolved = dict(mapping)
        for field, field_value in list(resolved.items()):
            resolved[field] = _resolve_spacing(field_value)
        styles[breakpoint] = Style(**resolved)

    return ResponsiveStyle(**styles)


def build_layout_style(
    default: ResponsiveStyle,
    props: dict[str, Any],
    responsive: dict[str, dict[str, Any]] | None = None,
    style: Style | ResponsiveStyle | None = None,
) -> Style | ResponsiveStyle:
    spacing = spacing_style(props)

    if responsive is not None:
        responsive_value = responsive_style(responsive)
        base = (default.base or Style()).merge(spacing)
        responsive_value = ResponsiveStyle(
            base=base.merge(responsive_value.base) if responsive_value.base else base,
            sm=responsive_value.sm,
            md=responsive_value.md,
            lg=responsive_value.lg,
            xl=responsive_value.xl,
        )
    else:
        responsive_value = ResponsiveStyle(
            base=(default.base or Style()).merge(spacing),
            sm=default.sm,
            md=default.md,
            lg=default.lg,
            xl=default.xl,
        )

    if style is None:
        return responsive_value

    if isinstance(style, ResponsiveStyle):
        return ResponsiveStyle(
            base=(responsive_value.base or Style()).merge(style.base),
            sm=style.sm if style.sm is not None else responsive_value.sm,
            md=style.md if style.md is not None else responsive_value.md,
            lg=style.lg if style.lg is not None else responsive_value.lg,
            xl=style.xl if style.xl is not None else responsive_value.xl,
        )

    if responsive is None:
        return style

    return ResponsiveStyle(
        base=(responsive_value.base or Style()).merge(style),
        sm=responsive_value.sm,
        md=responsive_value.md,
        lg=responsive_value.lg,
        xl=responsive_value.xl,
    )
