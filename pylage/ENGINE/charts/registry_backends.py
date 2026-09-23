"""Backend discovery and selection."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.charts.base import ChartBackend, ChartPayload
from pylage.ENGINE.charts.plotly_backend import get_plotly_backend

_BACKENDS: list[ChartBackend] = []


def _ensure_backends() -> None:
    if _BACKENDS:
        return
    plotly = get_plotly_backend()
    if plotly is not None:
        _BACKENDS.append(plotly)


def available_backends() -> list[str]:
    _ensure_backends()
    return [b.name for b in _BACKENDS]


def select_backend(figure: Any) -> ChartBackend:
    _ensure_backends()
    for backend in _BACKENDS:
        if backend.accept(figure):
            return backend
    raise TypeError(
        f"No chart backend accepts figure of type {type(figure)!r}. "
        f"Available backends: {available_backends() or ['(none — install plotly)']}"
    )


def figure_to_payload(
    figure: Any,
    *,
    config: dict[str, Any] | None = None,
) -> ChartPayload:
    backend = select_backend(figure)
    return backend.to_payload(figure, config=config)
