"""Tests for the high-level native pl.chart(data=...) API."""

from __future__ import annotations

import json

import pytest

import pylage as pl
from pylage.ENGINE.components.chart import Chart


plotly = pytest.importorskip("plotly")
import plotly.graph_objects as go


ROWS = [
    {"month": "Jan", "sales": 10, "profit": 3, "city": "A", "size": 8},
    {"month": "Feb", "sales": 20, "profit": 7, "city": "B", "size": 12},
    {"month": "Mar", "sales": 15, "profit": 5, "city": "A", "size": 10},
]


def _payload(chart: Chart) -> dict:
    return json.loads(chart.props["_chart_payload"].value)


def test_native_bar_chart():
    chart = pl.chart(
        data=ROWS,
        type="bar",
        x="month",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["backend"] == "plotly"
    assert len(payload["data"]) == 1
    assert payload["data"][0]["type"] == "bar"
    assert payload["data"][0]["x"] == ["Jan", "Feb", "Mar"]
    assert payload["data"][0]["y"] == [10, 20, 15]


def test_native_line_chart():
    chart = pl.chart(
        data=ROWS,
        type="line",
        x="month",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["data"][0]["type"] == "scatter"
    assert payload["data"][0]["mode"] == "lines"


def test_native_scatter_chart():
    chart = pl.chart(
        data=ROWS,
        type="scatter",
        x="month",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["data"][0]["type"] == "scatter"
    assert payload["data"][0]["mode"] == "markers"


def test_native_area_chart():
    chart = pl.chart(
        data=ROWS,
        type="area",
        x="month",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["data"][0]["type"] == "scatter"
    assert payload["data"][0]["mode"] == "lines"
    assert payload["data"][0]["fill"] == "tozeroy"


def test_native_pie_chart():
    chart = pl.chart(
        data=ROWS,
        type="pie",
        x="city",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["data"][0]["type"] == "pie"
    assert payload["data"][0]["labels"] == ["A", "B", "A"]
    assert payload["data"][0]["values"] == [10, 20, 15]


def test_native_multiple_y_columns():
    chart = pl.chart(
        data=ROWS,
        type="line",
        x="month",
        y=["sales", "profit"],
    )

    payload = _payload(chart)

    assert len(payload["data"]) == 2
    assert payload["data"][0]["name"] == "sales"
    assert payload["data"][1]["name"] == "profit"


def test_native_color_groups_cartesian_chart():
    chart = pl.chart(
        data=ROWS,
        type="line",
        x="month",
        y="sales",
        color="city",
    )

    payload = _payload(chart)

    assert len(payload["data"]) == 2
    assert {trace["name"] for trace in payload["data"]} == {"A", "B"}


def test_native_scatter_size():
    chart = pl.chart(
        data=ROWS,
        type="scatter",
        x="month",
        y="sales",
        size="size",
    )

    payload = _payload(chart)

    assert payload["data"][0]["marker"]["size"] == [8, 12, 10]


def test_native_axis_labels():
    chart = pl.chart(
        data=ROWS,
        type="line",
        x="month",
        y="sales",
        x_label="Month",
        y_label="Sales",
    )

    payload = _payload(chart)

    assert payload["layout"]["xaxis"]["title"]["text"] == "Month"
    assert payload["layout"]["yaxis"]["title"]["text"] == "Sales"


def test_native_default_type_is_line():
    chart = pl.chart(
        data=ROWS,
        x="month",
        y="sales",
    )

    payload = _payload(chart)

    assert payload["data"][0]["type"] == "scatter"
    assert payload["data"][0]["mode"] == "lines"


def test_native_missing_x_is_rejected():
    with pytest.raises(TypeError, match="requires 'x'"):
        pl.chart(
            data=ROWS,
            type="bar",
            y="sales",
        )


def test_native_missing_y_is_rejected():
    with pytest.raises(TypeError, match="requires 'y'"):
        pl.chart(
            data=ROWS,
            type="bar",
            x="month",
        )


def test_native_missing_column_is_rejected():
    with pytest.raises(KeyError, match="Unknown y column"):
        pl.chart(
            data=ROWS,
            type="bar",
            x="month",
            y="missing",
        )


def test_native_invalid_type_is_rejected():
    with pytest.raises(ValueError, match="Unsupported chart kind"):
        pl.chart(
            data=ROWS,
            type="invalid",
            x="month",
            y="sales",
        )


def test_figure_and_data_are_mutually_exclusive():
    fig = go.Figure(
        data=[go.Bar(x=["A"], y=[1])]
    )

    with pytest.raises(TypeError, match="either 'figure' or 'data'"):
        pl.chart(
            fig,
            data=ROWS,
            type="bar",
            x="month",
            y="sales",
        )


def test_existing_plotly_figure_api_remains_supported():
    fig = go.Figure(
        data=[go.Bar(x=["A", "B"], y=[1, 2])]
    )

    chart = pl.chart(fig)
    payload = _payload(chart)

    assert payload["backend"] == "plotly"
    assert payload["data"][0]["type"] == "bar"
    assert payload["data"][0]["x"] == ["A", "B"]
    assert payload["data"][0]["y"] == [1, 2]


def test_native_chart_produces_json_safe_payload():
    chart = pl.chart(
        data=ROWS,
        type="bar",
        x="month",
        y="sales",
    )

    json.dumps(_payload(chart))
