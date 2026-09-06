import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Dashboard Grid", level=2),
        pl.text("High-level responsive grid arrangements for multi-widget operational views."),
        ui.stat_group(
            ui.metric(label="Total Visits", value="1.4M", delta="+12%"),
            ui.metric(label="Avg Duration", value="4m 12s", delta="+24s"),
            ui.metric(label="Conversion", value="3.8%", delta="+0.4%"),
            columns=3,
        ),
        ui.dashboard_grid(
            ui.card(
                heading="Quarterly Performance",
                body="Revenue is tracking 14% ahead of projection for Q3 across all territories.",
                footer="Updated 5m ago",
                variant="elevated",
            ),
            ui.card(
                heading="System Alerts",
                body="All node clusters healthy. Zero critical incidents reported in the last 48 hours.",
                footer="Status: Green",
                variant="outlined",
            ),
            layout="2-col",
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
