from __future__ import annotations

from typing import Any

from pylage.ENGINE import State, Style
from pylage.ENGINE.core.component import component
from pylage.ENGINE.core.registry import PropDefinition, registry


registry.register_if_missing(
    "Textarea",
    "textarea",
    props={
        "value": PropDefinition(
            "value",
            kind="text",
        ),
        "placeholder": PropDefinition(
            "placeholder",
            kind="attribute",
            html_name="placeholder",
        ),
        "name": PropDefinition(
            "name",
            kind="attribute",
            html_name="name",
        ),
        "rows": PropDefinition(
            "rows",
            kind="attribute",
            html_name="rows",
        ),
        "cols": PropDefinition(
            "cols",
            kind="attribute",
            html_name="cols",
        ),
        "disabled": PropDefinition(
            "disabled",
            kind="boolean",
            html_name="disabled",
        ),
        "required": PropDefinition(
            "required",
            kind="boolean",
            html_name="required",
        ),
        "readonly": PropDefinition(
            "readonly",
            kind="boolean",
            html_name="readonly",
        ),
        "title": PropDefinition(
            "title",
            kind="attribute",
            html_name="title",
        ),
        "minlength": PropDefinition(
            "minlength",
            kind="attribute",
            html_name="minlength",
        ),
        "maxlength": PropDefinition(
            "maxlength",
            kind="attribute",
            html_name="maxlength",
        ),
    },
)


_BASE_STYLE = Style(
    width="100%",
    box_sizing="border-box",
    min_height="120px",
    padding="0.625rem 0.75rem",
    font_size="1rem",
    line_height="1.5",
    color="var(--color-text)",
    background_color="var(--color-background)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-md)",
    transition="border-color 150ms ease, box-shadow 150ms ease",
)


def textarea(
    value: Any = "",
    *,
    style: Style | None = None,
    **props: Any,
):
    """Create a public PyLage UI textarea using the existing renderer."""

    if isinstance(value, State) and "on_input" not in props:

        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

        props["on_input"] = update_state

    return component(
        "Textarea",
        value=value,
        style=_BASE_STYLE.merge(style),
        **props,
    )


__all__ = ["textarea"]
