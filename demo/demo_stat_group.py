import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Stat Group", level=2),
        pl.text("Responsive KPI grid patterns for executives and analytics dashboards."),
        ui.stat_group(
            ui.metric(label="Total Revenue", value="₹1,24,000", delta="+18.2%", description="vs preceding period"),
            ui.metric(label="Active Subscriptions", value="8,420", delta="+6.1%", description="14 new today"),
            ui.metric(label="Bounce Rate", value="24.3%", delta="-3.4%", description="Lower is better"),
            ui.metric(label="Server Uptime", value="99.99%", delta="0.0%", description="All systems operational"),
            columns=4,
        ),
        pl.heading("Quick Mapping Definition", level=3),
        ui.stat_group(
            items=[
                {"label": "Direct Traffic", "value": "45.2K", "delta": "+12%"},
                {"label": "Referral Leads", "value": "18.9K", "delta": "+4%"},
                {"label": "Organic Search", "value": "62.1K", "delta": "+22%"},
            ],
            columns=3,
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
