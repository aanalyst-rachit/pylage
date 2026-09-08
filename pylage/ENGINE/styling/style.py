from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Style:
    """Structured CSS style definition for PyLage components."""

    color: Any = None
    background: Any = None
    background_color: Any = None

    font_size: Any = None
    font_weight: Any = None
    font_family: Any = None
    line_height: Any = None
    text_align: Any = None
    content: Any = None

    margin: Any = None
    margin_top: Any = None
    margin_right: Any = None
    margin_bottom: Any = None
    margin_left: Any = None

    padding: Any = None
    padding_top: Any = None
    padding_right: Any = None
    padding_bottom: Any = None
    padding_left: Any = None

    width: Any = None
    min_width: Any = None
    max_width: Any = None

    height: Any = None
    min_height: Any = None
    max_height: Any = None

    display: Any = None
    position: Any = None
    top: Any = None
    right: Any = None
    bottom: Any = None
    left: Any = None

    flex_direction: Any = None
    flex_wrap: Any = None
    justify_content: Any = None
    align_items: Any = None
    align_content: Any = None
    flex: Any = None
    flex_grow: Any = None
    flex_shrink: Any = None
    flex_basis: Any = None

    gap: Any = None
    row_gap: Any = None
    column_gap: Any = None

    grid_template_columns: Any = None
    grid_template_rows: Any = None
    grid_column: Any = None
    grid_row: Any = None

    border: Any = None
    border_width: Any = None
    border_style: Any = None
    border_color: Any = None
    border_radius: Any = None

    box_shadow: Any = None
    opacity: Any = None
    overflow: Any = None
    overflow_x: Any = None
    overflow_y: Any = None
    box_sizing: Any = None
    cursor: Any = None
    object_fit: Any = None
    object_position: Any = None
    aspect_ratio: Any = None
    user_select: Any = None
    text_overflow: Any = None
    word_break: Any = None
    overflow_wrap: Any = None
    hyphens: Any = None

    z_index: Any = None
    transform: Any = None
    transition: Any = None
    text_transform: Any = None
    text_decoration: Any = None
    letter_spacing: Any = None
    white_space: Any = None
    outline: Any = None
    visibility: Any = None
    pointer_events: Any = None

    border_top: Any = None
    border_right: Any = None
    border_bottom: Any = None
    border_left: Any = None

    custom: dict[str, Any] | None = None
    pseudo: dict[str, "Style"] | None = None

    def merge(self, override: "Style | None") -> "Style":
        """Return a new Style with override values taking precedence."""

        if override is None:
            return self

        if not isinstance(override, Style):
            raise TypeError("override must be a Style or None")

        values = {}

        for field_name in self.__dataclass_fields__:
            if field_name in {"custom", "pseudo"}:
                continue

            value = getattr(override, field_name)

            if value is None:
                value = getattr(self, field_name)

            values[field_name] = value

        custom = dict(self.custom or {})
        custom.update(override.custom or {})
        values["custom"] = custom or None

        pseudo = dict(self.pseudo or {})
        for selector, override_style in (override.pseudo or {}).items():
            base_style = pseudo.get(selector)
            pseudo[selector] = (
                override_style
                if base_style is None
                else base_style.merge(override_style)
            )
        values["pseudo"] = pseudo or None

        return Style(**values)

    def to_css(self) -> str:
        """Convert the style definition into a CSS declaration string."""

        # Import lazily to avoid a styling -> core import cycle.
        from pylage.ENGINE.core.state import State

        declarations: list[str] = []

        for field_name, value in self.__dict__.items():
            if field_name in {"custom", "pseudo"}:
                continue

            if isinstance(value, State):
                value = value.value

            if value is None:
                continue

            css_name = _css_name(field_name)
            declarations.append(
                f"{css_name}:{value}"
            )

        for name, value in (self.custom or {}).items():
            if isinstance(value, State):
                value = value.value

            if value is None:
                continue

            if not isinstance(name, str) or not name.startswith("--"):
                raise ValueError(
                    "custom CSS property names must start with '--'"
                )

            declarations.append(
                f"{name}:{value}"
            )

        return ";".join(declarations)

    def to_pseudo_css(self, selector: str) -> str:
        """Convert pseudo-class and pseudo-element styles into scoped CSS rules."""
        if not isinstance(selector, str) or not selector:
            raise ValueError("selector must be a non-empty string")

        rules: list[str] = []
        pseudo_elements = {"before", "after"}

        for pseudo_name, style in (self.pseudo or {}).items():
            if not isinstance(pseudo_name, str) or not pseudo_name:
                raise ValueError("pseudo selectors must be non-empty strings")

            if not isinstance(style, Style):
                raise TypeError("pseudo values must be Style instances")

            css = style.to_css()
            if not css:
                continue

            css = ";".join(
                f"{declaration} {chr(33)}important"
                for declaration in css.split(";")
                if declaration
            )
            separator = "::" if pseudo_name in pseudo_elements else ":"
            rules.append(f"{selector}{separator}{pseudo_name}{{{css}}}")

        return "".join(rules)


def _css_name(name: str) -> str:
    """Convert Python snake_case names into CSS kebab-case names."""

    return name.replace("_", "-")
