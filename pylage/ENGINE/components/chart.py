"""First-class Chart component for PyLage."""

from __future__ import annotations

import json
from typing import Any

from pylage.ENGINE.charts.dataframe import dataframe_to_figure
from pylage.ENGINE.charts.plotly_backend import is_plotly_available
from pylage.ENGINE.charts.registry_backends import figure_to_payload
from pylage.ENGINE.core.component import Component, component
from pylage.ENGINE.core.registry import PropDefinition, registry
from pylage.ENGINE.core.state import State


def _unwrap(value: Any) -> Any:
    if isinstance(value, State):
        return value.value
    return value


def _payload_to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, separators=(",", ":"))


def _chart_renderer(renderer: Any, component: Component) -> str:
    from html import escape

    common = renderer._render_common_attributes(component)
    attributes = renderer._render_prop_attributes(
        component,
        excluded={
            "figure", "config", "text", "children",
            "height", "width", "_chart_payload",
        },
    )

    raw = _unwrap(component.props.get("_chart_payload"))
    if isinstance(raw, dict):
        payload = raw
        payload_json = _payload_to_json(raw)
    elif isinstance(raw, str) and raw:
        payload_json = raw
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"backend": "none", "data": [], "layout": {}, "config": {}}
    else:
        payload = {
            "backend": "none",
            "data": [],
            "layout": {"title": {"text": "No chart data"}},
            "config": {},
        }
        payload_json = _payload_to_json(payload)

    height = component.props.get("height", "400px")
    width = component.props.get("width", "100%")
    if isinstance(height, (int, float)):
        height = f"{height}px"
    if isinstance(width, (int, float)):
        width = f"{width}px"

    style_bits = [f"width:{width}", f"height:{height}", "min-height:200px"]
    existing_style = component.props.get("style")
    if existing_style:
        style_bits.append(str(existing_style))

    style_attr = f' style="{escape(";".join(style_bits))}"'
    backend = payload.get("backend", "plotly") if isinstance(payload, dict) else "plotly"

    if "role=" not in attributes:
        attributes += ' role="img"'

    if "aria-label=" not in attributes:
        accessible_title = component.props.get("title")
        if accessible_title is None and isinstance(payload, dict):
            layout = payload.get("layout")
            if isinstance(layout, dict):
                payload_title = layout.get("title")
                if isinstance(payload_title, dict):
                    accessible_title = payload_title.get("text")
                elif isinstance(payload_title, str):
                    accessible_title = payload_title

        if accessible_title is None:
            accessible_title = "Chart"

        attributes += (
            ' aria-label="'
            + escape(str(accessible_title), quote=True)
            + '"'
        )

    return (
        f'<div {common}{attributes}'
        f' data-pylage-chart="1"'
        f' data-chart-backend="{escape(str(backend))}"'
        f' data-chart-payload="{escape(payload_json)}"'
        f'{style_attr}>'
        f'</div>'
    )


def _register_chart() -> None:
    registry.register_if_missing(
        "Chart",
        "div",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
            "aria_label": PropDefinition(
                "aria_label",
                kind="attribute",
                html_name="aria-label",
            ),
            "role": PropDefinition(
                "role",
                kind="attribute",
                html_name="role",
            ),
            "height": PropDefinition("height", kind="attribute"),
            "width": PropDefinition("width", kind="attribute"),
            "visible": PropDefinition(
                "visible",
                kind="boolean",
                html_name="hidden",
                boolean_mode="inverse",
            ),
            # JSON *string* so client setAttribute works
            "_chart_payload": PropDefinition(
                "_chart_payload",
                kind="attribute",
                html_name="data-chart-payload",
                reactive=True,
            ),
            "figure": PropDefinition(
                "figure",
                kind="attribute",
                html_name=None,
                reactive=False,
            ),
            "config": PropDefinition(
                "config",
                kind="attribute",
                html_name=None,
                reactive=False,
            ),
        },
        renderer=_chart_renderer,
    )


def _build_payload_dict(
    figure: Any,
    config: dict[str, Any] | None,
    *,
    data: Any = None,
    chart_type: str | None = None,
    x: str | None = None,
    y: str | list[str] | tuple[str, ...] | None = None,
    color: str | None = None,
    size: str | None = None,
    name: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
) -> dict[str, Any]:
    resolved = _unwrap(figure)

    if resolved is None and data is not None:
        resolved = dataframe_to_figure(
            _unwrap(data),
            x=x,
            y=y,
            kind=chart_type or "line",
            color=color,
            size=size,
            name=name,
            allow_extended=True,
        )

        if x_label is not None:
            resolved.update_layout(xaxis_title=x_label)

        if y_label is not None:
            resolved.update_layout(yaxis_title=y_label)

    if resolved is None:
        return {
            "backend": "none",
            "data": [],
            "layout": {"title": {"text": "No chart data"}},
            "config": {},
        }

    if not is_plotly_available():
        raise ImportError(
            "Chart requires plotly. Install with:\n"
            "  pip install 'pylage[charts]'   or   pip install plotly"
        )

    return figure_to_payload(resolved, config=config).to_dict()


def Chart(
    figure: Any = None,
    *,
    data: Any = None,
    type: str | None = None,
    x: str | None = None,
    y: str | list[str] | tuple[str, ...] | None = None,
    color: str | None = None,
    size: str | None = None,
    name: str | None = None,
    x_label: str | None = None,
    y_label: str | None = None,
    config: dict[str, Any] | None = None,
    height: Any = 400,
    width: Any = "100%",
    class_name: str | None = None,
    title: str | None = None,
    **props: Any,
) -> Component:
    """Interactive Chart component.

    High-level data API::

        pl.chart(data=df, type="line", x="month", y="sales")

    ``data`` accepts pandas/Polars DataFrames, list-of-records, or
    column mappings. Supported chart types are ``line``, ``bar``,
    ``scatter``, ``area``, and ``pie``.

    ``figure`` remains supported as the advanced Plotly escape hatch::

        pl.chart(fig)

    ``figure`` and ``data`` are mutually exclusive.

    Native charts also support ``color``, ``size`` (scatter), ``name``,
    ``x_label``, and ``y_label``.

    Supported events (via on_* kwargs):
      on_click(payload)    – plotly_click points
      on_select(payload)   – plotly_selected points/range
      on_hover(payload)    – plotly_hover points
      on_relayout(payload) – zoom/pan relayout
    """
    _register_chart()

    if figure is not None and data is not None:
        raise TypeError(
            "Chart accepts either 'figure' or 'data', not both."
        )

    if data is not None:
        if x is None:
            raise TypeError(
                "Chart data API requires 'x'."
            )
        if y is None:
            raise TypeError(
                "Chart data API requires 'y'."
            )
        if type is None:
            type = "line"

    if data is not None:
        # Native API validation errors are part of the public contract and
        # must not be silently converted into an empty/error chart.
        initial_dict = _build_payload_dict(
            figure,
            config,
            data=data,
            chart_type=type,
            x=x,
            y=y,
            color=color,
            size=size,
            name=name,
            x_label=x_label,
            y_label=y_label,
        )
    else:
        # Preserve the existing advanced Plotly/figure behavior, including
        # safe rendering when an invalid figure is supplied.
        try:
            initial_dict = _build_payload_dict(
                figure,
                config,
                x_label=x_label,
                y_label=y_label,
            )
        except (ImportError, TypeError):
            initial_dict = {
                "backend": "none",
                "data": [],
                "layout": {"title": {"text": "Chart error"}},
                "config": {},
            }
    # Store as JSON string — required for differential prop updates
    payload_state = State(_payload_to_json(initial_dict))

    chart_props: dict[str, Any] = {
        "height": height,
        "width": width,
        "_chart_payload": payload_state,
        "config": config or {},
    }
    if class_name is not None:
        chart_props["class_name"] = class_name
    if title is not None:
        chart_props["title"] = title
    chart_props.update(props)

    chart = component("Chart", **chart_props)

    if isinstance(figure, State):
        def _on_figure_change(_old: Any, new: Any) -> None:
            try:
                payload_state.set(
                    _payload_to_json(
                        _build_payload_dict(
                            new,
                            config,
                            data=data,
                            chart_type=type,
                            x=x,
                            y=y,
                            color=color,
                            size=size,
                            name=name,
                            x_label=x_label,
                            y_label=y_label,
                        )
                    )
                )
            except (ImportError, TypeError):
                payload_state.set(
                    _payload_to_json({
                        "backend": "none",
                        "data": [],
                        "layout": {"title": {"text": "Chart error"}},
                        "config": {},
                    })
                )

        unsubscribe = figure.subscribe(_on_figure_change)
        chart.add_cleanup(unsubscribe)

    return chart


chart = Chart
