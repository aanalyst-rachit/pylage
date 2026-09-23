"""Plotly backend adapter (first production backend)."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.charts.base import ChartBackend, ChartPayload


def is_plotly_available() -> bool:
    try:
        import plotly  # noqa: F401
        return True
    except ImportError:
        return False


class PlotlyBackend(ChartBackend):
    name = "plotly"

    def accept(self, figure: Any) -> bool:
        if figure is None:
            return False
        # Accept plotly.graph_objects.Figure and plotly.express figures
        # (express returns graph_objects.Figure under the hood).
        try:
            from plotly.graph_objs import Figure
            return isinstance(figure, Figure)
        except ImportError:
            return False

    def to_payload(
        self,
        figure: Any,
        *,
        config: dict[str, Any] | None = None,
    ) -> ChartPayload:
        if not self.accept(figure):
            raise TypeError(
                "PlotlyBackend only accepts plotly.graph_objs.Figure "
                f"(got {type(figure)!r})"
            )

        # Use Plotly's own JSON serialization path.
        # to_plotly_json() produces pure JSON-safe structures.
        fig_dict = figure.to_plotly_json()

        data = fig_dict.get("data", [])
        layout = fig_dict.get("layout", {})
        frames = fig_dict.get("frames")

        # Default config focused on interactivity without toolbar bloat
        # for embedded dashboards. Users can override via config=.
        default_config: dict[str, Any] = {
            "responsive": True,
            "displayModeBar": True,
            "displaylogo": False,
            "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        }
        if config:
            default_config.update(config)

        return ChartPayload(
            backend=self.name,
            data=data if isinstance(data, list) else [],
            layout=layout if isinstance(layout, dict) else {},
            config=default_config,
            frames=frames if isinstance(frames, list) else None,
        )

    def capabilities(self) -> dict[str, bool]:
        return {
            "click": True,
            "hover": True,
            "select": True,
            "relayout": True,
            "zoom": True,
        }


def get_plotly_backend() -> PlotlyBackend | None:
    if not is_plotly_available():
        return None
    return PlotlyBackend()
