from __future__ import annotations

from html import escape
from typing import Any

from pyskin.core.component import Component
from pyskin.core.state import State
from pyskin.core.registry import registry


class HTMLRenderer:
    """Render a PySkin component tree into HTML."""

    def __init__(self) -> None:
        self._register_builtin_renderers()

    @property
    def registry(self):
        return registry

    def _register_builtin_renderers(self) -> None:
        """Attach built-in rendering callbacks to registry definitions."""

        builtins = {
            "Column": lambda renderer, component:
                renderer._render_column(component),

            "Heading": lambda renderer, component:
                renderer._render_heading(component),

            "Button": lambda renderer, component:
                renderer._render_button(component),

            "Input": lambda renderer, component:
                renderer._render_input(component),
        }

        for component_type, renderer_callback in builtins.items():
            definition = self.registry.get(component_type)

            if definition is None:
                continue

            if definition.renderer is not None:
                continue

            self.registry.set_renderer(
                component_type,
                renderer_callback,
            )

    def _value(self, value: Any) -> Any:
        """Resolve reactive State values."""
        if isinstance(value, State):
            return value.value
        return value

    def render(self, component: Component) -> str:
        return self._render_component(component)

    def _event_attributes(self, component: Component) -> str:
        if not component.events:
            return ""

        events = ",".join(
            escape(event, quote=True)
            for event in component.events
        )

        return f' data-pyskin-events="{events}"'

    def _render_children(self, component: Component) -> str:
        return "".join(
            self._render_component(child)
            for child in component.children
            if isinstance(child, Component)
        )

    def _render_common_attributes(
        self,
        component: Component,
    ) -> str:
        component_id = escape(component.id, quote=True)

        return (
            f'data-pyskin-id="{component_id}"'
            f'{self._event_attributes(component)}'
        )

    def _render_prop_attributes(
        self,
        component: Component,
        excluded: set[str] | None = None,
    ) -> str:
        """Render component props using registry metadata."""
        excluded = excluded or set()

        definition = self.registry.get(component.type)
        prop_definitions = (
            definition.props
            if definition is not None and definition.props is not None
            else {}
        )

        attributes: list[str] = []

        for name, raw_value in component.props.items():
            if name in excluded:
                continue

            value = self._value(raw_value)

            if value is None:
                continue

            prop_definition = prop_definitions.get(name)

            # Registry metadata controls the HTML attribute name.
            if prop_definition is not None:
                html_name = prop_definition.html_name or name
                kind = prop_definition.kind
            else:
                # Unknown props remain backward-compatible.
                html_name = {
                    "class_name": "class",
                    "html_for": "for",
                }.get(name, name)
                kind = "attribute"

            if kind == "boolean":
                if value:
                    attributes.append(
                        escape(html_name, quote=True)
                    )
                continue

            if value is True:
                attributes.append(
                    escape(html_name, quote=True)
                )
                continue

            attributes.append(
                f'{escape(html_name, quote=True)}='
                f'"{escape(str(value), quote=True)}"'
            )

        if not attributes:
            return ""

        return " " + " ".join(attributes)

    def _render_column(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        children = self._render_children(component)

        return (
            f'<div {common} '
            f'style="display:flex;flex-direction:column;">'
            f'{children}</div>'
        )

    def _render_heading(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "")
        )

        return (
            f"<h1 {common}>"
            f"{escape(str(text))}"
            f"</h1>"
        )

    def _render_input(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        value = self._value(
            component.props.get("value", "")
        )

        if component.events:
            events = self._event_attributes(component)
        else:
            events = ' data-pyskin-events="input,change"'

        return (
            f'<input {common}{events} '
            f'value="{escape(str(value), quote=True)}">'
        )

    def _render_button(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "Button")
        )

        attributes = common

        value = self._value(
            component.props.get("value")
        )

        disabled = self._value(
            component.props.get("disabled")
        )

        title = self._value(
            component.props.get("title")
        )

        if value is not None:
            attributes += (
                f' value="{escape(str(value), quote=True)}"'
            )

        if disabled:
            attributes += " disabled"

        if title is not None:
            attributes += (
                f' title="{escape(str(title), quote=True)}"'
            )

        return (
            f"<button {attributes}>"
            f"{escape(str(text))}"
            f"</button>"
        )

    def _render_component(self, component: Component) -> str:
        component_type = component.type

        definition = self.registry.get(component_type)

        if definition is None:
            tag = "div"
        else:
            tag = definition.tag

        common = self._render_common_attributes(component)
        children = self._render_children(component)

        # ---------------------------------------------------------
        # Custom registered renderer
        # ---------------------------------------------------------
        if definition is not None and definition.renderer is not None:
            return definition.renderer(self, component)

        # ---------------------------------------------------------
        # Generic component
        # ---------------------------------------------------------
        # Unknown components still render instead of disappearing.
        # Their children and normal props remain available.
        generic_attributes = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        if definition is not None and definition.void:
            return (
                f"<{tag} {common}"
                f"{generic_attributes}>"
            )

        text = self._value(
            component.props.get("text")
        )

        if text is not None:
            children = escape(str(text)) + children

        return (
            f"<{tag} {common}"
            f"{generic_attributes}>"
            f"{children}"
            f"</{tag}>"
        )


def render(component: Component) -> str:
    """Convenience function for rendering a component tree."""
    return HTMLRenderer().render(component)
