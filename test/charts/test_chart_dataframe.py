"""Tests for DataFrame-to-chart conversion."""

from __future__ import annotations

import json
from datetime import datetime

import pytest

from pylage.ENGINE.charts.dataframe import dataframe_to_figure
from pylage.ENGINE.charts.registry_backends import figure_to_payload


def test_record_list_converts_to_plotly_figure():
    rows = [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
    ]

    fig = dataframe_to_figure(
        rows,
        x="category",
        y="value",
        kind="bar",
    )

    assert len(fig.data) == 1
    assert list(fig.data[0].x) == ["A", "B"]
    assert list(fig.data[0].y) == [10, 20]


def test_column_mapping_converts_to_plotly_figure():
    data = {
        "category": ["A", "B"],
        "value": [10, 20],
    }

    fig = dataframe_to_figure(
        data,
        x="category",
        y="value",
    )

    assert list(fig.data[0].x) == ["A", "B"]
    assert list(fig.data[0].y) == [10, 20]


def test_nan_and_null_values_become_none():
    rows = [
        {"x": "A", "y": 1.0},
        {"x": "B", "y": float("nan")},
        {"x": "C", "y": None},
    ]

    fig = dataframe_to_figure(rows, x="x", y="y")

    assert list(fig.data[0].y) == [1.0, None, None]


def test_datetime_values_are_normalized_to_iso_strings():
    rows = [
        {"date": datetime(2026, 1, 1, 12, 30), "value": 10},
        {"date": datetime(2026, 1, 2, 12, 30), "value": 20},
    ]

    fig = dataframe_to_figure(rows, x="date", y="value")

    assert list(fig.data[0].x) == [
        "2026-01-01T12:30:00",
        "2026-01-02T12:30:00",
    ]


def test_infinite_float_values_become_none():
    rows = [
        {"x": "A", "y": float("inf")},
        {"x": "B", "y": float("-inf")},
    ]

    fig = dataframe_to_figure(rows, x="x", y="y")

    assert list(fig.data[0].y) == [None, None]


def test_numpy_scalar_values_are_normalized_when_numpy_is_available():
    np = pytest.importorskip("numpy")

    rows = [
        {"x": np.int64(1), "y": np.float64(2.5)},
    ]

    fig = dataframe_to_figure(rows, x="x", y="y")

    assert list(fig.data[0].x) == [1]
    assert list(fig.data[0].y) == [2.5]


def test_dataframe_conversion_preserves_generic_chart_backend_boundary():
    rows = [
        {"category": "A", "value": 10},
        {"category": "B", "value": 20},
    ]

    fig = dataframe_to_figure(rows, x="category", y="value")
    payload = figure_to_payload(fig).to_dict()

    assert payload["backend"] == "plotly"
    assert isinstance(payload["data"], list)
    json.dumps(payload)


def test_missing_x_column_is_rejected():
    with pytest.raises(KeyError, match="Unknown x column"):
        dataframe_to_figure(
            [{"value": 10}],
            x="missing",
            y="value",
        )


def test_missing_y_column_is_rejected():
    with pytest.raises(KeyError, match="Unknown y column"):
        dataframe_to_figure(
            [{"category": "A"}],
            x="category",
            y="missing",
        )


def test_unsupported_chart_kind_is_rejected():
    with pytest.raises(ValueError, match="Supported kinds"):
        dataframe_to_figure(
            [{"x": "A", "y": 1}],
            x="x",
            y="y",
            kind="pie",
        )


def test_unsupported_input_is_rejected():
    with pytest.raises(TypeError, match="Unsupported chart data"):
        dataframe_to_figure(
            "not tabular data",
            x="x",
            y="y",
        )


def test_real_pandas_dataframe_conversion():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({
        "category": pd.Series(
            ["A", "B", "C"],
            dtype="category",
        ),
        "date": pd.to_datetime([
            "2026-01-01",
            "2026-01-02",
            "2026-01-03",
        ]),
        "value": [10.0, 20.0, 30.0],
    })

    fig = dataframe_to_figure(
        df,
        x="date",
        y="value",
        kind="bar",
    )

    assert list(fig.data[0].x) == [
        "2026-01-01T00:00:00",
        "2026-01-02T00:00:00",
        "2026-01-03T00:00:00",
    ]
    assert list(fig.data[0].y) == [10.0, 20.0, 30.0]


def test_real_pandas_dataframe_handles_missing_values():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({
        "x": ["A", "B", "C"],
        "value": [10.0, float("nan"), None],
    })

    fig = dataframe_to_figure(
        df,
        x="x",
        y="value",
    )

    assert list(fig.data[0].y) == [10.0, None, None]


def test_real_pandas_categorical_values_are_supported():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({
        "category": pd.Categorical(["Consumer", "Business"]),
        "value": [10, 20],
    })

    fig = dataframe_to_figure(
        df,
        x="category",
        y="value",
        kind="bar",
    )

    assert list(fig.data[0].x) == ["Consumer", "Business"]
    assert list(fig.data[0].y) == [10, 20]


def test_real_pandas_dataframe_payload_is_json_safe():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({
        "date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "value": [1.0, 2.0],
    })

    fig = dataframe_to_figure(df, x="date", y="value")
    payload = figure_to_payload(fig).to_dict()

    json.dumps(payload)
    assert payload["backend"] == "plotly"
