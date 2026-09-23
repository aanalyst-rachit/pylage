"""Multi-chart dashboard demo."""

from __future__ import annotations

import pylage as pl
import plotly.graph_objects as go


def line_fig():
    fig = go.Figure(data=[go.Scatter(x=list(range(1, 13)), y=[3, 4, 2, 6, 5, 8, 7, 9, 8, 10, 11, 12], mode="lines+markers")])
    fig.update_layout(title="Trend", margin=dict(l=30, r=10, t=40, b=30), height=280)
    return fig


def pie_fig():
    fig = go.Figure(data=[go.Pie(labels=["A", "B", "C", "D"], values=[30, 25, 25, 20], hole=0.4)])
    fig.update_layout(title="Share", margin=dict(l=10, r=10, t=40, b=10), height=280)
    return fig


def scatter_fig():
    fig = go.Figure(data=[go.Scatter(x=[1, 2, 3, 4, 5, 6], y=[2, 3, 1, 5, 4, 6], mode="markers", marker=dict(size=12))])
    fig.update_layout(title="Correlation", margin=dict(l=30, r=10, t=40, b=30), height=280)
    return fig


def get_app():
    return pl.column(
        pl.heading("Charts Dashboard"),
        pl.text("Line · Donut · Scatter — all via pl.chart"),
        pl.row(
            pl.card(pl.chart(line_fig(), height=300)),
            pl.card(pl.chart(pie_fig(), height=300)),
            style=pl.style(gap="1rem", flex_wrap="wrap"),
        ),
        pl.card(pl.chart(scatter_fig(), height=300)),
        style=pl.style(padding="1.5rem", gap="1rem", max_width="1100px", margin="0 auto"),
    )


if __name__ == "__main__":
    pl.run(app_factory=get_app, title="Charts Dashboard", host="127.0.0.1", port=3001, serve=True)
