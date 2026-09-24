import json
from time import perf_counter

import plotly.graph_objects as go

from pylage.ENGINE.charts.base import ChartPayload
from pylage.ENGINE.charts.plotly_backend import PlotlyBackend
from pylage.ENGINE.core.state import State
from pylage.ENGINE.core.binding import StateBinding
from pylage.ENGINE.components.chart import _payload_to_json


# Phase 12 timing thresholds are derived from five controlled local
# benchmark runs: observed maximum + 50% regression margin.
PHASE12_THRESHOLDS = {
    "figure_conversion_s": 0.00337,
    "serialization_s": 0.00070,
    "multiple_chart_conversion_s": 0.05020,
    "repeated_conversion_s": 0.00331,
    "payload_deduplication_s": 0.00384,
    "chart_batching_per_update_s": 0.01602,
    "payload_bytes": 11168,
    "chart_batching_cycles": 1,
}


def _build_figure(points: int = 100) -> go.Figure:
    return go.Figure(
        data=[
            go.Scatter(
                x=list(range(points)),
                y=list(range(points)),
                mode="lines+markers",
                name="benchmark",
            )
        ]
    )


def _measure(fn, iterations: int = 100):
    start = perf_counter()

    for _ in range(iterations):
        fn()

    elapsed = perf_counter() - start

    return {
        "total": elapsed,
        "per_operation": elapsed / iterations,
    }


def _figure_to_payload(figure: go.Figure) -> ChartPayload:
    return PlotlyBackend().to_payload(figure)


def test_phase12_figure_conversion_benchmark():
    figure = _build_figure()

    result = _measure(
        lambda: _figure_to_payload(figure),
        iterations=100,
    )

    payload = _figure_to_payload(figure)

    assert payload.backend == "plotly"
    assert isinstance(payload.data, list)
    assert isinstance(payload.layout, dict)
    assert result["total"] >= 0
    assert result["per_operation"] >= 0
    assert result["per_operation"] <= PHASE12_THRESHOLDS["figure_conversion_s"]

    print()
    print("===== PHASE 12 — FIGURE CONVERSION =====")
    print("iterations        : 100")
    print(f"total             : {result['total']:.9f}s")
    print(f"per conversion    : {result['per_operation']:.9f}s")


def test_phase12_serialization_benchmark():
    figure = _build_figure()
    payload = _figure_to_payload(figure).to_dict()

    result = _measure(
        lambda: _payload_to_json(payload),
        iterations=100,
    )

    serialized = _payload_to_json(payload)

    assert isinstance(serialized, str)
    assert json.loads(serialized)["backend"] == "plotly"
    assert result["total"] >= 0
    assert result["per_operation"] >= 0
    assert result["per_operation"] <= PHASE12_THRESHOLDS["serialization_s"]

    print()
    print("===== PHASE 12 — PAYLOAD SERIALIZATION =====")
    print("iterations        : 100")
    print(f"total             : {result['total']:.9f}s")
    print(f"per serialization : {result['per_operation']:.9f}s")


def test_phase12_payload_size():
    figure = _build_figure()
    payload = _figure_to_payload(figure).to_dict()
    serialized = _payload_to_json(payload)

    payload_bytes = len(serialized.encode("utf-8"))

    assert payload_bytes > 0
    assert payload_bytes <= PHASE12_THRESHOLDS["payload_bytes"]

    print()
    print("===== PHASE 12 — PROTOCOL PAYLOAD SIZE =====")
    print(f"payload bytes     : {payload_bytes}")
    print(f"payload KiB       : {payload_bytes / 1024:.3f}")


def test_phase12_multiple_chart_conversion():
    figures = [_build_figure() for _ in range(10)]

    result = _measure(
        lambda: [_figure_to_payload(figure) for figure in figures],
        iterations=10,
    )

    payloads = [_figure_to_payload(figure) for figure in figures]

    assert len(payloads) == 10
    assert all(payload.backend == "plotly" for payload in payloads)
    assert result["total"] >= 0
    assert result["per_operation"] <= PHASE12_THRESHOLDS["multiple_chart_conversion_s"]

    print()
    print("===== PHASE 12 — MULTIPLE CHART CONVERSION =====")
    print("charts per batch  : 10")
    print("iterations        : 10")
    print(f"total             : {result['total']:.9f}s")
    print(f"per batch         : {result['per_operation']:.9f}s")


def test_phase12_repeated_conversion():
    figure = _build_figure()

    result = _measure(
        lambda: _figure_to_payload(figure),
        iterations=1000,
    )

    payload = _figure_to_payload(figure)

    assert payload.backend == "plotly"
    assert result["total"] >= 0
    assert result["per_operation"] >= 0
    assert result["per_operation"] <= PHASE12_THRESHOLDS["repeated_conversion_s"]

    print()
    print("===== PHASE 12 — REPEATED CONVERSION =====")
    print("iterations        : 1000")
    print(f"total             : {result['total']:.9f}s")
    print(f"per conversion    : {result['per_operation']:.9f}s")


def test_phase12_payload_deduplication_benchmark():
    import plotly.graph_objects as go

    figure = go.Figure(
        data=[
            go.Scatter(
                x=list(range(100)),
                y=list(range(100)),
                mode="lines",
                name="dedup",
            )
        ]
    )

    backend = PlotlyBackend()

    start = perf_counter()
    payloads = []

    for _ in range(100):
        payload = backend.to_payload(figure).to_dict()
        payloads.append(_payload_to_json(payload))

    elapsed = perf_counter() - start

    unique_payloads = len(set(payloads))
    payload_size = len(payloads[0].encode("utf-8"))

    print()
    print("===== PHASE 12 — PAYLOAD DEDUPLICATION =====")
    print(f"iterations          : {len(payloads)}")
    print(f"total               : {elapsed:.9f}s")
    print(f"per conversion      : {elapsed / len(payloads):.9f}s")
    print(f"unique payloads     : {unique_payloads}")
    print(f"payload bytes       : {payload_size}")
    print(
        f"repeated payloads   : "
        f"{len(payloads) - unique_payloads}"
    )

    assert len(payloads) == 100
    assert unique_payloads == 1
    assert elapsed / len(payloads) <= PHASE12_THRESHOLDS["payload_deduplication_s"]


def test_phase12_chart_batching_benchmark():
    import plotly.graph_objects as go

    from pylage import Chart
    from pylage.ENGINE.core.dirty import DirtyNodes
    from pylage.ENGINE.core.scheduler import Scheduler

    def make_figure(value):
        return go.Figure(
            data=[
                go.Scatter(
                    x=list(range(100)),
                    y=[value + i for i in range(100)],
                    mode="lines",
                    name="batch",
                )
            ]
        )

    figure_state = State(make_figure(0))
    chart = Chart(figure_state)

    dirty = DirtyNodes()
    processed = []

    scheduler = Scheduler(
        dirty,
        lambda node: processed.append(node),
    )

    StateBinding(
        chart,
        lambda component, props: None,
        dirty=dirty,
        scheduler=scheduler,
    )

    count = 100

    start = perf_counter()

    for value in range(1, count + 1):
        figure_state.set(make_figure(value))

    scheduler.flush()

    elapsed = perf_counter() - start

    print()
    print("===== PHASE 12 — CHART BATCHING =====")
    print(f"figure updates      : {count}")
    print(f"processing cycles   : {len(processed)}")
    print(f"elapsed             : {elapsed:.9f}s")
    print(f"per figure update   : {elapsed / count:.9f}s")

    assert figure_state.value.data[0].y[0] == 100
    assert len(processed) == PHASE12_THRESHOLDS["chart_batching_cycles"]
    assert elapsed / count <= PHASE12_THRESHOLDS["chart_batching_per_update_s"]
