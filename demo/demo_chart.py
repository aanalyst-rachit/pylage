"""Interactive chart demo — reactive + click events."""

from __future__ import annotations

import pylage as pl
import plotly.graph_objects as go


def get_app():
    values = pl.state([4, 2, 7, 5, 9])
    last_click = pl.state("Click a bar…")

    def make_figure(vals):
        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Jan", "Feb", "Mar", "Apr", "May"],
                    y=list(vals),
                    marker_color="#3b82f6",
                )
            ]
        )
        fig.update_layout(
            title="Monthly Revenue",
            margin=dict(l=40, r=20, t=50, b=40),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        return fig

    def bump():
        values.set([v + 1 for v in list(values.value)])

    def reset():
        values.set([4, 2, 7, 5, 9])

    def on_bar_click(payload):
        points = (payload or {}).get("points") or []
        if not points:
            last_click.set("Click a bar…")
            return
        p = points[0]
        last_click.set(f"Clicked {p.get('x')} → y={p.get('y')}")

    figure = pl.derived(values, compute=lambda v: make_figure(v))

    return pl.column(
        pl.heading("PyLage Chart Demo"),
        pl.text("Reactive Plotly chart + click events."),
        pl.row(
            pl.button("Bump values", on_click=bump),
            pl.button("Reset", on_click=reset),
            style=pl.style(gap="0.75rem", margin_bottom="1rem"),
        ),
        pl.text(last_click),
        pl.chart(figure, height=420, width="100%", on_click=on_bar_click),
        style=pl.style(padding="1.5rem", max_width="900px", margin="0 auto"),
    )


if __name__ == "__main__":
    pl.run(
        app_factory=get_app,
        title="PyLage Chart Demo",
        host="127.0.0.1",
        port=3000,
        serve=True,
    )
