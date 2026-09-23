"""Chart event wiring (component.events)."""

from __future__ import annotations

import pytest

plotly = pytest.importorskip("plotly")
import plotly.graph_objects as go

from pylage.ENGINE.components.chart import Chart


def test_on_click_registered():
    calls = []

    def handler(payload):
        calls.append(payload)

    fig = go.Figure(data=[go.Bar(x=["a"], y=[1])])
    c = Chart(fig, on_click=handler)
    assert "click" in c.events
    c.events["click"]({"points": [{"x": "a", "y": 1}]})
    assert len(calls) == 1
