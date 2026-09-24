"""DataFrame-to-chart conversion helpers.

Pandas and Polars remain optional dependencies. This module converts
tabular data into a Plotly Figure; the existing generic chart backend
pipeline remains responsible for figure -> ChartPayload conversion.
"""

from __future__ import annotations

import math
from datetime import date, datetime, time
from typing import Any


def _is_missing(value: Any) -> bool:
    """Return True for common null/NaN scalar values."""
    if value is None:
        return True

    try:
        result = value != value  # noqa: PLR0124
    except Exception:  # noqa: BLE001
        return False

    return isinstance(result, bool) and result


def _normalize_scalar(value: Any) -> Any:
    """Convert a tabular scalar into a JSON-safe chart scalar."""
    if _is_missing(value):
        return None

    if isinstance(value, (datetime, date, time)):
        return value.isoformat()

    # pandas Timestamp / Timedelta and similar scalar types expose
    # isoformat() without requiring pandas as a dependency.
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        try:
            return isoformat()
        except (TypeError, ValueError):
            pass

    # numpy scalar values expose item(); keep numpy optional.
    item = getattr(value, "item", None)
    if callable(item):
        try:
            scalar = item()
        except (TypeError, ValueError):
            scalar = value
        if scalar is not value:
            return _normalize_scalar(scalar)

    # Avoid leaking infinities into JSON/chart payloads.
    if isinstance(value, float) and not math.isfinite(value):
        return None

    return value


def _records_from_data(data: Any) -> tuple[list[str], list[dict[str, Any]]]:
    """Normalize supported tabular inputs into column names and records."""
    # pandas DataFrame-like
    if hasattr(data, "columns") and hasattr(data, "to_dict"):
        try:
            columns = [str(column) for column in data.columns]
            records = data.to_dict(orient="records")
            return columns, [
                {
                    column: _normalize_scalar(record.get(original))
                    for column, original in zip(columns, data.columns)
                }
                for record in records
            ]
        except (TypeError, ValueError, AttributeError):
            pass

    # Polars DataFrame-like.
    if hasattr(data, "columns") and hasattr(data, "rows"):
        try:
            columns = [str(column) for column in data.columns]
            rows = data.rows()
            return columns, [
                {
                    column: _normalize_scalar(value)
                    for column, value in zip(columns, row)
                }
                for row in rows
            ]
        except (TypeError, ValueError, AttributeError):
            pass

    # list/tuple of records
    if isinstance(data, (list, tuple)) and (
        not data or all(isinstance(item, dict) for item in data)
    ):
        columns = list(
            dict.fromkeys(
                str(key)
                for item in data
                for key in item
            )
        )
        return columns, [
            {
                column: _normalize_scalar(
                    next(
                        (
                            value
                            for key, value in item.items()
                            if str(key) == column
                        ),
                        None,
                    )
                )
                for column in columns
            }
            for item in data
        ]

    # dict[column -> sequence]
    if isinstance(data, dict):
        columns = [str(column) for column in data]
        values = [list(data[column]) for column in data]
        row_count = max((len(values_for_column) for values_for_column in values), default=0)
        records = []
        for index in range(row_count):
            records.append({
                column: _normalize_scalar(
                    values[column_index][index]
                    if index < len(values[column_index])
                    else None
                )
                for column_index, column in enumerate(columns)
            })
        return columns, records

    raise TypeError(
        "Unsupported chart data. Expected a pandas DataFrame, Polars "
        "DataFrame/LazyFrame, list of records, or column mapping."
    )


def dataframe_to_figure(
    data: Any,
    *,
    x: str,
    y: str | list[str] | tuple[str, ...],
    kind: str = "scatter",
    color: str | None = None,
    allow_extended: bool = False,
    size: str | None = None,
    name: str | None = None,
) -> Any:
    """Convert supported tabular data into a Plotly Figure.

    This is the internal adapter behind the high-level ``pl.chart(data=...)``
    API. ``x`` and ``y`` identify columns in the normalized tabular data.

    Supported kinds are ``line``, ``bar``, ``scatter``, ``area``, and ``pie``.
    Multiple ``y`` columns create multiple traces for line/bar/area charts.
    ``color`` creates one trace per category for supported Cartesian charts.
    ``size`` controls marker size for scatter charts.
    """
    try:
        import plotly.graph_objects as go
    except ImportError as exc:
        raise ImportError(
            "dataframe_to_figure requires plotly. Install with:\n"
            "  pip install 'pylage[charts]'   or   pip install plotly"
        ) from exc

    columns, records = _records_from_data(data)

    if x not in columns:
        raise KeyError(f"Unknown x column: {x!r}")

    if isinstance(y, str):
        y_columns = [y]
    elif isinstance(y, (list, tuple)):
        y_columns = list(y)
    else:
        raise TypeError(
            "Chart y must be a column name or a list/tuple of column names."
        )

    if not y_columns:
        raise ValueError("Chart y must contain at least one column.")

    for y_column in y_columns:
        if y_column not in columns:
            raise KeyError(f"Unknown y column: {y_column!r}")

    supported = {"scatter", "bar"}
    if allow_extended:
        supported.update({"line", "area", "pie"})

    if kind not in supported:
        raise ValueError(
            f"Unsupported chart kind {kind!r}. "
            "Supported kinds: 'scatter', 'bar'."
        )

    if kind == "pie":
        if len(y_columns) != 1:
            raise ValueError(
                "Pie charts require exactly one y column."
            )

        y_column = y_columns[0]
        return go.Figure(
            data=[
                go.Pie(
                    labels=[record[x] for record in records],
                    values=[record[y_column] for record in records],
                    name=name,
                )
            ]
        )

    traces = []

    if color is not None:
        if color not in columns:
            raise KeyError(f"Unknown color column: {color!r}")

        color_values = []
        for record in records:
            value = record[color]
            if value not in color_values:
                color_values.append(value)

        for color_value in color_values:
            filtered = [
                record for record in records
                if record[color] == color_value
            ]

            for y_column in y_columns:
                x_values = [record[x] for record in filtered]
                y_values = [record[y_column] for record in filtered]

                trace_name = (
                    str(color_value)
                    if len(y_columns) == 1
                    else f"{color_value} · {y_column}"
                )

                if kind == "line":
                    traces.append(
                        go.Scatter(
                            x=x_values,
                            y=y_values,
                            mode="lines",
                            name=trace_name,
                        )
                    )
                elif kind == "bar":
                    traces.append(
                        go.Bar(
                            x=x_values,
                            y=y_values,
                            name=trace_name,
                        )
                    )
                elif kind == "area":
                    traces.append(
                        go.Scatter(
                            x=x_values,
                            y=y_values,
                            mode="lines",
                            fill="tozeroy",
                            name=trace_name,
                        )
                    )
                else:
                    marker = {}
                    if size is not None:
                        if size not in columns:
                            raise KeyError(f"Unknown size column: {size!r}")
                        marker["size"] = [
                            record[size] for record in filtered
                        ]

                    traces.append(
                        go.Scatter(
                            x=x_values,
                            y=y_values,
                            mode="markers",
                            marker=marker,
                            name=trace_name,
                        )
                    )

        return go.Figure(data=traces)

    for y_column in y_columns:
        x_values = [record[x] for record in records]
        y_values = [record[y_column] for record in records]

        if kind == "line":
            traces.append(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    name=name if len(y_columns) == 1 else y_column,
                )
            )
        elif kind == "bar":
            traces.append(
                go.Bar(
                    x=x_values,
                    y=y_values,
                    name=name if len(y_columns) == 1 else y_column,
                )
            )
        elif kind == "area":
            traces.append(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="lines",
                    fill="tozeroy",
                    name=name if len(y_columns) == 1 else y_column,
                )
            )
        else:
            marker = {}
            if size is not None:
                if size not in columns:
                    raise KeyError(f"Unknown size column: {size!r}")
                marker["size"] = [record[size] for record in records]

            traces.append(
                go.Scatter(
                    x=x_values,
                    y=y_values,
                    mode="markers",
                    marker=marker,
                    name=name if len(y_columns) == 1 else y_column,
                )
            )

    return go.Figure(data=traces)


__all__ = ["dataframe_to_figure"]
