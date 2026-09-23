"""Modern PyLage public Chart API example."""

import plotly.graph_objects as go
import pylage as pl


# ---------------------------------------------------------------------------
# Chart
# ---------------------------------------------------------------------------

fig = go.Figure(
    data=[
        go.Bar(
            x=["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            y=[120, 180, 150, 220, 260, 310],
            name="Revenue",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: %{y}<extra></extra>"
            ),
        )
    ]
)

fig.update_layout(
    title={
        "text": "Monthly Revenue",
        "font": {
            "size": 24,
        },
        "x": 0.02,
        "xanchor": "left",
    },
    xaxis={
        "title": "Month",
        "showgrid": False,
        "zeroline": False,
    },
    yaxis={
        "title": "Revenue",
        "showgrid": True,
        "zeroline": False,
    },
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin={
        "l": 55,
        "r": 25,
        "t": 75,
        "b": 55,
    },
)


# ---------------------------------------------------------------------------
# Public PyLage API
# ---------------------------------------------------------------------------

header = pl.column(
    pl.text(
        "Analytics Dashboard",
        style=pl.style(
            font_size="2rem",
            font_weight="800",
            margin_bottom="0.4rem",
        ),
    ),
    pl.text(
        "Interactive charts with the PyLage public API.",
        muted=True,
        style=pl.style(
            font_size="1rem",
            margin_bottom="0",
        ),
    ),
    style=pl.style(
        margin_bottom="1.5rem",
    ),
)


chart_card = pl.column(
    pl.text(
        "Revenue Overview",
        style=pl.style(
            font_size="1.1rem",
            font_weight="700",
            margin_bottom="0.25rem",
        ),
    ),
    pl.text(
        "Monthly performance for the first half of the year.",
        muted=True,
        style=pl.style(
            font_size="0.875rem",
            margin_bottom="1rem",
        ),
    ),
    pl.Chart(
        fig,
        height=480,
        width="100%",
    ),

    pl.text(
        "Revenue Overview — Minimal",
        style=pl.style(
            font_size="1.1rem",
            font_weight="700",
            margin_top="2rem",
            margin_bottom="0.25rem",
        ),
    ),
    pl.text(
        "Same chart with hover enabled but the modebar hidden.",
        muted=True,
        style=pl.style(
            font_size="0.875rem",
            margin_bottom="1rem",
        ),
    ),
    pl.Chart(
        fig,
        height=480,
        width="100%",
        config={
            "displayModeBar": False,
        },
    ),

    style=pl.style(
        background_color="white",
        border_width="1px",
        border_style="solid",
        border_color="rgba(148, 163, 184, 0.25)",
        border_radius="1.25rem",
        padding="1.25rem",
        box_shadow="0 10px 30px rgba(15, 23, 42, 0.08)",
    ),
)


page = pl.column(
    header,
    chart_card,
    style=pl.style(
        width="100%",
        max_width="1100px",
        margin="0 auto",
        padding="3rem 1.5rem",
        box_sizing="border-box",
    ),
)


app = pl.column(
    page,
    style=pl.style(
        min_height="100vh",
        background=(
            "linear-gradient("
            "135deg, "
            "#f8fafc 0%, "
            "#eef2ff 50%, "
            "#f8fafc 100%"
            ")"
        ),
        font_family=(
            "Inter, system-ui, -apple-system, "
            "BlinkMacSystemFont, Segoe UI, sans-serif"
        ),
    ),
)


pl.run(app, serve=True)
