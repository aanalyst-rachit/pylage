import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        ui.dashboard_header(
            title="Analytics Overview",
            description="Real-time traffic and performance metrics for production environment.",
            actions=[
                ui.button("Export CSV", variant="outline"),
                ui.button("Add Widget", variant="primary"),
            ],
        ),
        ui.stat_group(
            ui.metric(label="Active Sessions", value="14,280", delta="+8.2%"),
            ui.metric(label="Error Rate", value="0.04%", delta="-0.01%"),
            ui.metric(label="Response Time", value="240ms", delta="-12ms"),
            columns=3,
        ),
        gap="2rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
