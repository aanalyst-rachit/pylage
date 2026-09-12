from __future__ import annotations

from html import escape
import re
from typing import Any

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.state import State
from pylage.ENGINE.core.registry import registry
from pylage.ENGINE.styling import ResponsiveStyle, Style
from pylage.ENGINE.styling.collector import StyleCollector
from pylage.ENGINE.styling.foundation import CSS_FOUNDATION
from pylage.ENGINE.styling.global_theme import get_global_theme


def _validate_url_attribute(value: Any) -> str:
    """Validate URL-valued HTML attributes before escaping them."""
    text = str(value)
    probe = re.sub(r"[\x00-\x20]+", "", text)
    match = re.match(r"^([A-Za-z][A-Za-z0-9+.-]*):", probe)
    if match and match.group(1).lower() not in {"http", "https"}:
        raise ValueError("unsafe URL scheme")
    return text


class HTMLRenderer:
    """Render a PyLage component tree into HTML."""

    def __init__(
        self,
        registry_instance=None,
        theme=None,
    ) -> None:
        self._registry = registry_instance or registry
        self._theme = theme
        self._styles = StyleCollector()
        self._responsive_css: list[str] = []
        self._pseudo_css: list[str] = []
        self._register_builtin_renderers()

    @property
    def registry(self):
        return self._registry

    def _register_builtin_renderers(self) -> None:
        """Attach built-in rendering callbacks to registry definitions."""

        builtins = {
            "Column": lambda renderer, component:
                renderer._render_column(component),

            "Row": lambda renderer, component:
                renderer._render_row(component),

            "Dialog": lambda renderer, component:
                renderer._render_dialog(component),

            "Drawer": lambda renderer, component:
                renderer._render_drawer(component),

            "Table": lambda renderer, component:
                renderer._render_table(component),
            "DataFrame": lambda renderer, component:
                renderer._render_dataframe(component),

            "Form": lambda renderer, component:
                renderer._render_form(component),

            "Card": lambda renderer, component:
                renderer._render_card(component),

            "Badge": lambda renderer, component:
                renderer._render_badge(component),

            "Text": lambda renderer, component:
                renderer._render_text(component),

            "Heading": lambda renderer, component:
                renderer._render_heading(component),

            "Breadcrumbs": lambda renderer, component:
                renderer._render_breadcrumbs(component),

            "Button": lambda renderer, component:
                renderer._render_button(component),

            "Input": lambda renderer, component:
                renderer._render_input(component),

            "Spinner": lambda renderer, component:
                renderer._render_spinner(component),
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
        self._styles.clear()
        self._responsive_css = []
        self._pseudo_css = []

        built_in_css = self._built_in_css()
        if built_in_css:
            self._styles.add(built_in_css)

        theme = self._theme
        if theme is None:
            theme = get_global_theme()

        if theme is not None:
            theme_css = theme.to_css()
            if theme_css:
                self._styles.add(
                    f":root{{{theme_css}}}",
                    ' data-pylage-theme="true"',
                )

        html = self._render_component(component)

        if self._pseudo_css:
            self._styles.add("".join(self._pseudo_css))

        if self._responsive_css:
            self._styles.add("".join(self._responsive_css))

        return self._styles.render() + html

    def _built_in_css(self) -> str:
        """Return framework-level CSS for native HTML semantics."""
        return CSS_FOUNDATION

    def _event_attributes(self, component: Component) -> str:
        if not component.events:
            return ""

        events = ",".join(
            escape(event, quote=True)
            for event in component.events
        )

        return f' data-pylage-events="{events}"'

    def _render_children(self, component: Component) -> str:
        return "".join(
            self._render_component(child)
            for child in component.children
            if isinstance(child, Component)
        )

    def _render_common_attributes(
        self,
        component: Component,
        default_style: Style | None = None,
    ) -> str:
        component_id = escape(component.id, quote=True)

        attributes = (
            f'data-pylage-id="{component_id}"'
            f'{self._event_attributes(component)}'
        )

        style = component.props.get("style")

        if isinstance(style, State):
            style = style.value

        if default_style is not None:
            if style is None:
                style = default_style
            elif isinstance(style, Style):
                style = default_style.merge(style)

        if isinstance(style, ResponsiveStyle):
            css = style.to_base_css()

            if css:
                attributes += (
                    f' style="{escape(css, quote=True)}"'
                )

            pseudo_css = style.to_base_pseudo_css(
                f'[data-pylage-id="{component_id}"]'
            )
            if pseudo_css:
                self._styles.add(pseudo_css)

            responsive_css = style.to_responsive_css(
                f'[data-pylage-id="{component_id}"]'
            )

            if responsive_css:
                self._styles.add(responsive_css)

        elif style is not None:
            to_css = getattr(style, "to_css", None)

            if callable(to_css):
                css = to_css()

                if css:
                    attributes += (
                        f' style="{escape(css, quote=True)}"'
                    )

        if isinstance(style, Style):
            pseudo_css = style.to_pseudo_css(
                f'[data-pylage-id="{component_id}"]'
            )
            if pseudo_css:
                self._styles.add(pseudo_css)

        return attributes

    def _render_prop_attributes(
        self,
        component: Component,
        excluded: set[str] | None = None,
    ) -> str:
        """Render component props using registry metadata."""
        excluded = excluded or set()

        definition = self.registry.get(component.type)

        # Input-like components with fixed HTML input types.
        if component.type in {"Checkbox", "Switch"}:
            component.props.setdefault("_html_type", "checkbox")
        elif component.type == "Slider":
            component.props.setdefault("_html_type", "range")
        elif component.type == "DatePicker":
            component.props.setdefault("_html_type", "date")

        prop_definitions = (
            definition.props
            if definition is not None and definition.props is not None
            else {}
        )

        attributes: list[str] = []

        for name, raw_value in component.props.items():
            # ``style`` is rendered by _render_common_attributes().
            # Never emit it again as a generic HTML attribute.
            if name == "style" or name in excluded:
                continue

            if isinstance(raw_value, Component):
                raise TypeError(
                    f"Prop {name!r} received a Component instance {raw_value!r}. "
                    f"Pass components as children, not as props."
                )

            value = self._value(raw_value)

            if value is None:
                continue

            if isinstance(value, Component):
                raise TypeError(
                    f"Prop {name!r} resolved to a Component instance {value!r}. "
                    f"Pass components as children, not as props."
                )

            if callable(value) and not name.startswith("on_"):
                raise TypeError(
                    f"Prop {name!r} received a callable value {value!r}. "
                    f"Callables should only be passed to on_* event handlers."
                )

            prop_definition = prop_definitions.get(name)

            if name == "_html_type":
                html_name = "type"
                kind = "attribute"
            elif prop_definition is not None:
                html_name = prop_definition.html_name or name
                kind = prop_definition.kind
            else:
                # Unknown props remain backward-compatible.
                # HTML naming is owned by registry metadata.
                html_name = name
                kind = "attribute"

            if name == "_html_type":
                attributes.append(
                    f'type="{escape(str(value), quote=True)}"'
                )
                continue

            if kind == "boolean":
                boolean_mode = (
                    prop_definition.boolean_mode
                    if prop_definition is not None
                    else "normal"
                )

                dom_value = bool(value)

                if boolean_mode == "inverse":
                    dom_value = not dom_value

                if dom_value:
                    attributes.append(
                        escape(html_name, quote=True)
                    )
                continue

            if kind in {"text", "state"}:
                continue

            if value is False:
                continue

            if value is True:
                attributes.append(
                    escape(html_name, quote=True)
                )
                continue

            if (
                component.type in {"Image", "Video", "Audio"}
                and name == "src"
            ):
                value = _validate_url_attribute(value)

            attributes.append(
                f'{escape(html_name, quote=True)}='
                f'"{escape(str(value), quote=True)}"'
            )

        # RadioGroup contract: keep the selected radio marker
        # immediately after its value attribute.
        if (
            component.type == "Input"
            and component.props.get("_html_type") == "radio"
        ):
            value_attr = next(
                (attr for attr in attributes if attr.startswith("value=")),
                None,
            )
            checked_attr = next(
                (attr for attr in attributes if attr == "checked"),
                None,
            )

            if value_attr is not None and checked_attr is not None:
                attributes.remove(value_attr)
                attributes.remove(checked_attr)

                value_index = 0
                attributes.insert(value_index, checked_attr)
                attributes.insert(value_index, value_attr)

        if not attributes:
            return ""

        return " " + " ".join(attributes)

    def _spinner_css(self) -> str:
        """Return built-in CSS for the Spinner component."""
        return """
.pylage-spinner {
    display: inline-block;
    width: 1.5rem;
    height: 1.5rem;
    box-sizing: border-box;
    border: 0.2rem solid currentColor;
    border-right-color: transparent;
    border-radius: 50%;
    animation: pylage-spinner-spin 0.75s linear infinite;
}

.pylage-spinner[data-size="small"] {
    width: 1rem;
    height: 1rem;
    border-width: 0.15rem;
}

.pylage-spinner[data-size="large"] {
    width: 2rem;
    height: 2rem;
    border-width: 0.25rem;
}

@keyframes pylage-spinner-spin {
    to {
        transform: rotate(360deg);
    }
}
"""

    def _render_spinner(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        class_name = self._value(component.props.get("class_name"))
        title = self._value(component.props.get("title"))
        size = self._value(component.props.get("size"))
        text = self._value(component.props.get("text"))
        children = self._render_children(component)

        classes = ["pylage-spinner"]
        if class_name:
            custom_class = str(class_name)
            if custom_class != "pylage-spinner":
                classes.append(custom_class)

        attributes = (
            common
            + ' class="'
            + escape(" ".join(classes), quote=True)
            + '"'
        )

        if title is not None:
            attributes += f' title="{escape(str(title), quote=True)}"'

        if size is not None:
            attributes += f' data-size="{escape(str(size), quote=True)}"'

        attributes += self._render_prop_attributes(
            component,
            excluded={"children", "class_name", "title", "size", "text"},
        )

        content = "" if text is None else escape(str(text))
        self._styles.add(self._spinner_css())

        return f"<span {attributes}>{content}{children}</span>"

    def _drawer_css(self) -> str:
        """Return built-in CSS for the Drawer component."""
        return """
.pylage-drawer {
    position: fixed;
    top: 0;
    left: 0;
    width: 320px;
    max-width: calc(100vw - 32px);
    height: 100vh;
    max-height: 100vh;
    box-sizing: border-box;
    margin: 0;
    transform: translateX(-100%);
    visibility: hidden;
    pointer-events: none;
    transition:
        transform 180ms ease,
        visibility 180ms ease;
    z-index: 1000;
}

.pylage-drawer[open] {
    transform: translateX(0);
    visibility: visible;
    pointer-events: auto;
}
"""

    def _render_drawer(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        class_name = self._value(component.props.get("class_name"))
        title = self._value(component.props.get("title"))

        classes = ["pylage-drawer"]

        if class_name:
            custom_class = str(class_name)
            if custom_class != "pylage-drawer":
                classes.append(custom_class)

        attributes = (
            common
            + ' class="'
            + escape(" ".join(classes), quote=True)
            + '"'
        )

        if title is not None:
            attributes += (
                f' title="{escape(str(title), quote=True)}"'
            )

        attributes += self._render_prop_attributes(
            component,
            excluded={"children", "class_name", "title"},
        )

        children = self._render_children(component)

        self._styles.add(self._drawer_css())

        return (
            f"<aside {attributes}>"
            f"{children}"
            f"</aside>"
        )

    def _render_form(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        attributes = common + self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f"<form {attributes}>"
            f"{children}"
            f"</form>"
        )

    def _dataframe_css(self) -> str:
        """Return built-in CSS for the DataFrame component."""
        return """
.pylage-dataframe {
    width: 100%;
    overflow: hidden;
    box-sizing: border-box;
}

.pylage-dataframe__viewport {
    width: 100%;
    max-width: 100%;
    max-height: 480px;
    overflow: auto;
}

.pylage-dataframe__grid {
    width: max-content;
    min-width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    table-layout: auto;
    font-size: 14px;
    line-height: 1.4;
}

.pylage-dataframe__grid th,
.pylage-dataframe__grid td {
    box-sizing: border-box;
    padding: 8px 12px;
    min-width: 100px;
    max-width: 320px;
    border-right: 1px solid var(--color-border);
    border-bottom: 1px solid var(--color-border);
    background: var(--color-background);
    vertical-align: middle;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.pylage-dataframe__grid tr > :first-child {
    border-left: 1px solid var(--color-border);
}

.pylage-dataframe__grid thead th {
    position: sticky;
    top: 0;
    z-index: 3;
    background: var(--color-surface-variant);
    font-weight: 600;
    text-align: left;
}

.pylage-dataframe__corner {
    position: sticky !important;
    left: 0;
    z-index: 5 !important;
    width: 48px;
    min-width: 48px !important;
    max-width: 48px !important;
    padding: 8px !important;
    background: var(--color-surface-variant) !important;
}

.pylage-dataframe__row-number {
    position: sticky;
    left: 0;
    z-index: 2;
    width: 48px;
    min-width: 48px !important;
    max-width: 48px !important;
    padding: 8px !important;
    background: var(--color-surface-variant) !important;
    color: var(--color-text-muted);
    font-weight: 500;
    text-align: center;
}

.pylage-dataframe__cell--numeric {
    text-align: right;
    font-variant-numeric: tabular-nums;
}

.pylage-dataframe__grid tbody tr:hover td,
.pylage-dataframe__grid tbody tr:hover th {
    background: var(--color-surface-variant);
}

.pylage-dataframe--no-cell-border .pylage-dataframe__grid th,
.pylage-dataframe--no-cell-border .pylage-dataframe__grid td {
    border-right: 0;
    border-bottom: 0;
}

.pylage-dataframe--no-cell-border .pylage-dataframe__grid tr > :first-child {
    border-left: 0;
}

.pylage-dataframe__empty {
    padding: 16px;
    text-align: center;
    color: var(--color-text-muted);
}
"""

    def _render_dataframe(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        headers = self._value(component.props.get("headers"))
        data = self._value(component.props.get("data"))

        class_name = self._value(component.props.get("class_name"))
        title = self._value(component.props.get("title"))
        cell_border = self._value(
            component.props.get("cell_border", True)
        )

        classes = ["pylage-dataframe"]

        if not cell_border:
            classes.append("pylage-dataframe--no-cell-border")

        if class_name:
            custom_class = str(class_name)
            if custom_class != "pylage-dataframe":
                classes.append(custom_class)

        attributes = (
            common
            + ' class="'
            + escape(" ".join(classes), quote=True)
            + '"'
        )

        if title is not None:
            attributes += (
                f' title="{escape(str(title), quote=True)}"'
            )

        parts = [
            f"<div {attributes}>",
            '<div class="pylage-dataframe__viewport">',
            '<table class="pylage-dataframe__grid">',
        ]

        if data is not None:
            headers, rows = self._normalize_table_data(data, headers)

            parts.append("<thead><tr>")
            parts.append(
                '<th class="pylage-dataframe__corner" '
                'aria-hidden="true"></th>'
            )

            for index, header in enumerate(headers):
                parts.append(
                    f'<th class="pylage-dataframe__header" '
                    f'data-column-index="{index}">'
                    f'{escape(str(header))}'
                    "</th>"
                )

            parts.append("</tr></thead>")
            parts.append("<tbody>")

            for row_index, row in enumerate(rows, start=1):
                parts.append(
                    f'<tr class="pylage-dataframe__row" '
                    f'data-row-index="{row_index}">'
                )

                parts.append(
                    f'<th class="pylage-dataframe__row-number" '
                    f'scope="row">{row_index}</th>'
                )

                for column_index, cell in enumerate(row):
                    numeric = (
                        isinstance(cell, (int, float))
                        and not isinstance(cell, bool)
                    )

                    cell_class = (
                        "pylage-dataframe__cell "
                        "pylage-dataframe__cell--numeric"
                        if numeric
                        else "pylage-dataframe__cell"
                    )

                    parts.append(
                        f'<td class="{cell_class}" '
                        f'data-column-index="{column_index}">'
                        f'{escape(self._table_cell_text(cell))}'
                        "</td>"
                    )

                parts.append("</tr>")

            parts.append("</tbody>")

        else:
            parts.append(
                '<tbody><tr>'
                '<td class="pylage-dataframe__empty">'
                'No data'
                '</td>'
                '</tr></tbody>'
            )

        parts.extend([
            "</table>",
            "</div>",
            "</div>",
        ])

        self._styles.add(self._dataframe_css())

        return "".join(parts)

    def _render_table(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        headers = self._value(component.props.get("headers"))
        data = self._value(component.props.get("data"))

        table_attributes = common

        title = self._value(component.props.get("title"))
        if title is not None:
            table_attributes += f' title="{escape(str(title), quote=True)}"'

        class_name = self._value(component.props.get("class_name"))
        if class_name is not None:
            table_attributes += f' class="{escape(str(class_name), quote=True)}"'

        parts = [f"<table {table_attributes}>"]

        if data is not None:
            headers, rows = self._normalize_table_data(data, headers)

            if headers:
                parts.append("<thead><tr>")
                for header in headers:
                    parts.append(f"<th>{escape(str(header))}</th>")
                parts.append("</tr></thead>")

            parts.append("<tbody>")
            for row in rows:
                parts.append("<tr>")
                for cell in row:
                    parts.append(f"<td>{escape(self._table_cell_text(cell))}</td>")
                parts.append("</tr>")
            parts.append("</tbody>")
        else:
            for child in component.children:
                rendered = self._render_component(child)
                if rendered:
                    parts.append(rendered)

        parts.append("</table>")
        return "".join(parts)

    def _normalize_table_data(
        self,
        data: Any,
        headers: Any = None,
    ) -> tuple[list[Any], list[list[Any]]]:
        headers = list(headers) if headers is not None else None

        # pandas DataFrame
        if hasattr(data, "columns") and hasattr(data, "to_dict"):
            try:
                columns = list(data.columns)
                records = data.to_dict(orient="records")
                return (
                    headers or columns,
                    [[record.get(column) for column in columns] for record in records],
                )
            except (TypeError, ValueError):
                pass

        # polars DataFrame / LazyFrame-like objects
        if hasattr(data, "columns") and hasattr(data, "rows"):
            try:
                columns = list(data.columns)
                rows = [list(row) for row in data.rows()]
                return headers or columns, rows
            except (TypeError, ValueError):
                pass

        # Mapping of column -> values
        if isinstance(data, dict):
            columns = list(data.keys())
            values = [list(data[column]) for column in columns]
            row_count = max((len(values_for_column) for values_for_column in values), default=0)
            rows = [
                [
                    values[index] if index < len(values) else None
                    for values in values
                ]
                for index in range(row_count)
            ]
            return headers or columns, rows

        # List of record dictionaries
        if isinstance(data, (list, tuple)) and data and all(
            isinstance(item, dict) for item in data
        ):
            columns = headers or list(dict.fromkeys(
                key for item in data for key in item
            ))
            rows = [[item.get(column) for column in columns] for item in data]
            return columns, rows

        # Ordinary row-oriented sequences
        if isinstance(data, (list, tuple)):
            rows = [
                list(row) if isinstance(row, (list, tuple)) else [row]
                for row in data
            ]
            if headers is None and rows:
                headers = []
            return headers or [], rows

        return headers or [], [[data]]

    def _table_cell_text(self, value: Any) -> str:
        if value is None:
            return ""
        return str(value)

    def _render_dialog(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        attributes = common + self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f"<dialog {attributes}>"
            f"{children}"
            f"</dialog>"
        )

    def _render_column(self, component: Component) -> str:
        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="flex",
                flex_direction="column",
            ),
        )
        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        definition = self.registry.get(component.type)
        tag = definition.tag if definition is not None else "div"

        return (
            f'<{tag} {common}{props}>'
            f'{children}</{tag}>'
        )

    def _render_row(self, component: Component) -> str:
        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="flex",
                flex_direction="row",
            ),
        )
        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )
        children = self._render_children(component)

        return (
            f'<div {common}{props}>'
            f'{children}</div>'
        )

    def _render_card(self, component: Component) -> str:
        """Render Card using its registry-defined HTML tag."""

        common = self._render_common_attributes(
            component,
            default_style=Style(
                display="block",
                width="100%",
                box_sizing="border-box",
            ),
        )

        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )

        children = self._render_children(component)

        # Registry-defined text props become element content.
        text_values: list[str] = []

        definition = self.registry.get(component.type)

        if definition is not None and definition.props is not None:
            for prop_name, prop_definition in definition.props.items():
                if prop_definition.kind != "text":
                    continue

                value = component.props.get(prop_name)

                if value is None:
                    continue

                value = self._value(value)

                if value is not None:
                    text_values.append(escape(str(value)))

        if text_values:
            children = "".join(text_values) + children

        tag = definition.tag if definition is not None else "div"

        return (
            f'<{tag} {common}{props}>'
            f'{children}</{tag}>'
        )


    def _render_badge(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        props = self._render_prop_attributes(
            component,
            excluded={"children"},
        )

        children: list[str] = []

        for child in component.children:
            if not isinstance(child, Component):
                continue

            if child.type == "Text":
                child_common = self._render_common_attributes(child)
                child_props = self._render_prop_attributes(
                    child,
                    excluded={"text", "children"},
                )
                text = self._value(child.props.get("text", ""))
                children.append(
                    f"<span {child_common}{child_props}>"
                    f"{escape(str(text))}"
                    f"</span>"
                )
            else:
                children.append(self._render_component(child))

        return (
            f"<span {common}{props}>"
            f"{''.join(children)}"
            f"</span>"
        )


    def _render_text(self, component: Component) -> str:
        common = self._render_common_attributes(component)
        props = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        text = self._value(
            component.props.get("text", "")
        )

        return (
            f"<div {common}{props}>"
            f"{escape(str(text))}"
            f"</div>"
        )

    def _render_heading(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "")
        )

        definition = self.registry.get("Heading")
        tag = definition.tag if definition is not None else "h1"

        return (
            f"<{tag} {common}>"
            f"{escape(str(text))}"
            f"</{tag}>"
        )

    def _render_breadcrumbs(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        attributes = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        if attributes:
            attributes = " " + attributes

        items = "".join(
            f"<li>{self._render_component(child)}</li>"
            for child in component.children
            if isinstance(child, Component)
        )

        return (
            f'<nav {common}{attributes} aria-label="Breadcrumb">'
            f"<ol>{items}</ol>"
            f"</nav>"
        )

    def _render_input(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        attributes = self._render_prop_attributes(
            component,
            excluded={"children"},
        )

        return (
            f"<input {common}{attributes}>"
        )

    def _render_button(self, component: Component) -> str:
        common = self._render_common_attributes(component)

        text = self._value(
            component.props.get("text", "Button")
        )

        attributes = common + self._render_prop_attributes(
            component,
            excluded={"text", "children"},
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
        common = self._render_common_attributes(component)
        children = self._render_children(component)
        generic_attributes = self._render_prop_attributes(
            component,
            excluded={"text", "children"},
        )

        if definition is not None and definition.void:
            return (
                f"<{tag} {common}"
                f"{generic_attributes}>"
            )

        # Registry-defined text props become component content.
        text_values: list[str] = []

        if definition is not None and definition.props is not None:
            for prop_name, prop_definition in definition.props.items():
                if prop_definition.kind != "text":
                    continue

                value = component.props.get(prop_name)

                if value is None:
                    continue

                value = self._value(value)

                if value is not None:
                    text_values.append(escape(str(value)))

        # Backward-compatible generic text support.
        # A registered custom component such as:
        #     registry.register("Card", "section")
        # may provide props={"text": "Hello Card"} without
        # explicitly declaring a text PropDefinition.
        if not text_values and "text" in component.props:
            value = self._value(component.props.get("text"))

            if value is not None:
                text_values.append(escape(str(value)))

        if text_values:
            children = "".join(text_values) + children

        return (
            f"<{tag} {common}"
            f"{generic_attributes}>"
            f"{children}"
            f"</{tag}>"
        )


def render(component: Component) -> str:
    """Convenience function for rendering a component tree."""
    return HTMLRenderer().render(component)
