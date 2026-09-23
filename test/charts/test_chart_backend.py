"""Unit tests for chart backends and payload."""

from __future__ import annotations

import json
import pytest

plotly = pytest.importorskip("plotly")
import plotly.graph_objects as go
import plotly.express as px

from pylage.ENGINE.charts.plotly_backend import PlotlyBackend, is_plotly_available
from pylage.ENGINE.charts.registry_backends import figure_to_payload
from pylage.ENGINE.components.chart import Chart, _build_payload_dict, _payload_to_json
from pylage.ENGINE.core.renderer import render
from pylage.ENGINE.core.state import State


def test_plotly_available():
    assert is_plotly_available() is True


def test_backend_accepts_figure():
    backend = PlotlyBackend()
    fig = go.Figure(data=[go.Bar(x=["a"], y=[1])])
    assert backend.accept(fig) is True
    assert backend.accept({"not": "a figure"}) is False


def test_payload_roundtrip():
    fig = go.Figure(data=[go.Bar(x=["a", "b"], y=[1, 2])])
    fig.update_layout(title="T")
    payload = figure_to_payload(fig)
    d = payload.to_dict()
    assert d["backend"] == "plotly"
    assert len(d["data"]) == 1
    assert "layout" in d
    # JSON safe
    json.dumps(d)


def test_plotly_express_figure_converts_to_payload():
    fig = px.scatter(
        x=[10, 20, 30],
        y=[15, 25, 35],
        title="Plotly Express Test",
    )

    payload = figure_to_payload(fig).to_dict()

    assert payload["backend"] == "plotly"
    assert len(payload["data"]) == 1
    assert payload["data"][0]["type"] == "scatter"

    x_payload = payload["data"][0]["x"]
    y_payload = payload["data"][0]["y"]
    assert isinstance(x_payload, dict)
    assert isinstance(y_payload, dict)
    assert "dtype" in x_payload
    assert "bdata" in x_payload
    assert "dtype" in y_payload
    assert "bdata" in y_payload

    assert payload["layout"]["title"]["text"] == "Plotly Express Test"

    json.dumps(payload)


def test_pie_figure_converts_to_payload():
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["A", "B", "C"],
                values=[10, 20, 30],
            )
        ]
    )

    payload = figure_to_payload(fig).to_dict()

    assert payload["backend"] == "plotly"
    assert len(payload["data"]) == 1
    assert payload["data"][0]["type"] == "pie"
    assert payload["data"][0]["labels"] == ["A", "B", "C"]
    assert payload["data"][0]["values"] == [10, 20, 30]

    json.dumps(payload)


def test_area_figure_converts_to_payload():
    fig = go.Figure(
        data=[
            go.Scatter(
                x=["A", "B", "C"],
                y=[10, 20, 15],
                mode="lines",
                fill="tozeroy",
            )
        ]
    )

    payload = figure_to_payload(fig).to_dict()

    assert payload["backend"] == "plotly"
    assert len(payload["data"]) == 1
    assert payload["data"][0]["type"] == "scatter"
    assert payload["data"][0]["mode"] == "lines"
    assert payload["data"][0]["fill"] == "tozeroy"

    json.dumps(payload)


def test_multi_series_figure_preserves_all_traces():
    fig = go.Figure(
        data=[
            go.Bar(
                x=["A", "B", "C"],
                y=[10, 20, 30],
                name="Series A",
            ),
            go.Bar(
                x=["A", "B", "C"],
                y=[15, 25, 35],
                name="Series B",
            ),
        ]
    )

    payload = figure_to_payload(fig).to_dict()

    assert payload["backend"] == "plotly"
    assert len(payload["data"]) == 2

    assert payload["data"][0]["type"] == "bar"
    assert payload["data"][0]["name"] == "Series A"
    assert payload["data"][0]["y"] == [10, 20, 30]

    assert payload["data"][1]["type"] == "bar"
    assert payload["data"][1]["name"] == "Series B"
    assert payload["data"][1]["y"] == [15, 25, 35]

    json.dumps(payload)


def test_payload_preserves_frames():
    fig = go.Figure(
        data=[go.Scatter(x=[1, 2], y=[1, 2])]
    )

    fig.frames = [
        go.Frame(
            data=[go.Scatter(x=[1, 2], y=[2, 3])],
            name="frame-1",
        ),
        go.Frame(
            data=[go.Scatter(x=[1, 2], y=[3, 4])],
            name="frame-2",
        ),
    ]

    payload = figure_to_payload(fig)
    d = payload.to_dict()

    assert d["backend"] == "plotly"
    assert d["frames"] is not None
    assert len(d["frames"]) == 2
    assert d["frames"][0]["name"] == "frame-1"
    assert d["frames"][1]["name"] == "frame-2"

    # Frames must remain JSON-safe.
    json.dumps(d)


def test_chart_component_html():
    fig = go.Figure(data=[go.Scatter(x=[1, 2], y=[3, 4])])
    c = Chart(fig, height=300)
    html = render(c)
    assert 'data-pylage-chart="1"' in html
    assert "data-chart-payload=" in html
    assert "plotly" in html


def test_chart_renderer_malformed_payload_falls_back_safely():
    chart = Chart()
    chart.props["_chart_payload"].set('{"backend":"plotly","data":')

    html = render(chart)

    assert 'data-pylage-chart="1"' in html
    assert 'data-chart-backend="none"' in html
    assert "data-chart-payload=" in html


def test_chart_renderer_incomplete_payload_is_tolerated():
    chart = Chart()
    chart.props["_chart_payload"].set(
        json.dumps({"backend": "plotly"})
    )

    html = render(chart)

    assert 'data-pylage-chart="1"' in html
    assert 'data-chart-backend="plotly"' in html
    assert "data-chart-payload=" in html

def test_chart_reactive_state_payload():
    fig = go.Figure(data=[go.Bar(x=["x"], y=[1])])
    state = State(fig)
    c = Chart(state, height=200)
    assert isinstance(c.props["_chart_payload"], State)
    raw = c.props["_chart_payload"].value
    assert isinstance(raw, str)
    parsed = json.loads(raw)
    assert parsed["backend"] == "plotly"


def test_chart_reactive_state_updates_payload():
    initial = go.Figure(
        data=[go.Bar(x=["A"], y=[1])]
    )
    updated = go.Figure(
        data=[go.Bar(x=["B", "C"], y=[10, 20])]
    )

    state = State(initial)
    chart = Chart(state)

    initial_raw = chart.props["_chart_payload"].value
    initial_payload = json.loads(initial_raw)

    assert initial_payload["backend"] == "plotly"
    assert initial_payload["data"][0]["x"] == ["A"]
    assert initial_payload["data"][0]["y"] == [1]

    state.set(updated)

    updated_raw = chart.props["_chart_payload"].value
    updated_payload = json.loads(updated_raw)

    assert updated_payload["backend"] == "plotly"
    assert updated_payload["data"][0]["x"] == ["B", "C"]
    assert updated_payload["data"][0]["y"] == [10, 20]

    chart.cleanup()


def test_build_payload_none():
    d = _build_payload_dict(None, None)
    assert d["backend"] == "none"


def test_chart_reactive_subscription_is_cleaned_up():
    import plotly.graph_objects as go

    state = State(go.Figure())

    chart = Chart(state)

    # Chart creation registers exactly one reactive subscription.
    assert len(state._subscribers) == 1

    # Component cleanup must unsubscribe the Chart from the State.
    chart.cleanup()

    assert len(state._subscribers) == 0

    # Cleanup must be idempotent.
    chart.cleanup()

    assert len(state._subscribers) == 0


def test_chart_is_exported_from_top_level_public_api():
    namespace = {}
    exec("from pylage import *", namespace)

    assert "Chart" in namespace
    assert "chart" in namespace
    assert namespace["Chart"] is namespace["chart"]

def test_plotly_config_defaults_and_overrides():
    fig = go.Figure(data=[go.Bar(x=["a"], y=[1])])

    payload = figure_to_payload(
        fig,
        config={
            "displayModeBar": False,
            "responsive": False,
            "customFlag": True,
        },
    )

    config = payload.to_dict()["config"]

    # User values override backend defaults.
    assert config["displayModeBar"] is False
    assert config["responsive"] is False

    # Existing backend defaults remain unless overridden.
    assert config["displaylogo"] is False
    assert "modeBarButtonsToRemove" in config

    # Custom Plotly config is preserved.
    assert config["customFlag"] is True


def test_plotly_backend_rejects_unsupported_figure():
    backend = PlotlyBackend()

    with pytest.raises(TypeError, match="PlotlyBackend only accepts"):
        backend.to_payload({"not": "a figure"})


def test_registry_rejects_unsupported_figure():
    with pytest.raises(TypeError, match="No chart backend accepts figure"):
        figure_to_payload({"not": "a figure"})

def test_chart_payload_is_deterministic_json():
    fig = go.Figure(
        data=[
            go.Bar(
                x=["A", "B"],
                y=[10, 20],
            )
        ]
    )
    payload = figure_to_payload(fig).to_dict()

    first = _payload_to_json(payload)
    second = _payload_to_json(payload)

    assert first == second
    assert json.loads(first) == payload


def test_chart_payload_round_trips_through_update_message_json():
    from pylage.ENGINE.core.protocol import UpdateMessage

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[1, 2],
                y=[3, 4],
                mode="lines",
            )
        ]
    )

    payload = figure_to_payload(fig).to_dict()
    message = UpdateMessage(
        component_id="chart-1",
        props={"_chart_payload": _payload_to_json(payload)},
    )

    decoded = UpdateMessage.from_json(message.to_json())

    assert decoded.component_id == "chart-1"
    assert json.loads(decoded.props["_chart_payload"]) == payload


def test_chart_payload_round_trips_through_messagepack():
    from pylage.ENGINE.core.protocol import UpdateMessage
    from pylage.ENGINE.core.protocol_codec import decode_message, encode_message

    fig = go.Figure(
        data=[
            go.Bar(
                x=["A", "B"],
                y=[5, 15],
            )
        ]
    )

    payload = figure_to_payload(fig).to_dict()
    message = UpdateMessage(
        component_id="chart-2",
        props={"_chart_payload": _payload_to_json(payload)},
    )

    encoded = encode_message(message)
    decoded = decode_message(encoded)

    assert decoded.component_id == message.component_id
    assert decoded.props == message.props
    assert decoded.remove_props == []
    assert decoded.prop_meta is None
    assert json.loads(decoded.props["_chart_payload"]) == payload


def test_chart_payload_malformed_json_is_rejected_by_update_protocol():
    from pylage.ENGINE.core.protocol import UpdateMessage

    malformed = '{"type":"update","id":"chart-1","props":'

    with pytest.raises(ValueError, match="Invalid JSON update message"):
        UpdateMessage.from_json(malformed)


def test_chart_payload_preserves_nested_json_data():
    from pylage.ENGINE.core.protocol import UpdateMessage
    from pylage.ENGINE.core.protocol_codec import decode_message, encode_message

    payload = {
        "backend": "plotly",
        "data": [
            {
                "type": "scatter",
                "x": [1, 2, 3],
                "y": [4.5, 5.5, 6.5],
                "meta": {
                    "labels": ["first", "second"],
                    "enabled": True,
                    "missing": None,
                },
            }
        ],
        "layout": {
            "title": {
                "text": "Nested payload",
            }
        },
        "config": {
            "responsive": True,
        },
        "frames": [],
    }

    message = UpdateMessage(
        component_id="chart-nested",
        props={
            "_chart_payload": _payload_to_json(payload),
        },
    )

    decoded = decode_message(encode_message(message))

    assert decoded.component_id == message.component_id
    assert decoded.props == message.props
    assert decoded.remove_props == []
    assert decoded.prop_meta is None
    assert json.loads(decoded.props["_chart_payload"]) == payload


def test_chart_payload_uses_existing_asgi_message_size_boundary():
    import asyncio
    from pylage.ENGINE.core.protocol import UpdateMessage
    from pylage.ENGINE.runtime.asgi import _ASGIConnection

    payload = {
        "backend": "plotly",
        "data": [
            {
                "type": "scatter",
                "x": list(range(2000)),
                "y": list(range(2000)),
            }
        ],
        "layout": {},
        "config": {},
    }

    message = UpdateMessage(
        component_id="chart-oversized",
        props={
            "_chart_payload": _payload_to_json(payload),
        },
    )

    encoded = message.to_json().encode("utf-8")
    assert len(encoded) > 1024

    messages = []
    received = False

    async def receive():
        nonlocal received
        if not received:
            received = True
            return {
                "type": "websocket.receive",
                "text": message.to_json(),
            }
        return {"type": "websocket.disconnect"}

    async def send(message):
        messages.append(message)

    connection = _ASGIConnection(
        receive,
        send,
        max_message_size=1024,
    )

    async def scenario():
        await connection.__anext__()

    with pytest.raises(StopAsyncIteration):
        asyncio.run(scenario())

    assert messages == [
        {"type": "websocket.close", "code": 1009},
    ]


def test_chart_payload_rejects_non_json_python_values():
    def dangerous_function():
        return "executed"

    payload = {
        "backend": "plotly",
        "data": [],
        "layout": {},
        "config": {
            "callable": dangerous_function,
            "object": object(),
        },
    }

    with pytest.raises(TypeError, match="not JSON serializable"):
        _payload_to_json(payload)
