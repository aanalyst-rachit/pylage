import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        ui.dashboard_header(
            title="System Operations",
            description="Active nodes and cluster telemetry.",
        ),
        ui.dashboard_section(
            ui.metric_grid(
                ui.metric(label="Nodes Online", value="64/64", delta="100%"),
                ui.metric(label="Memory Pressure", value="42%", delta="-3%"),
                ui.metric(label="Network Inbound", value="1.2 Gbps", delta="+0.1"),
                columns=3,
            ),
            title="Telemetry Overview",
            description="Aggregated vitals from primary and secondary edge clusters.",
            action=ui.button("Refresh", variant="outline"),
        ),
        ui.dashboard_section(
            ui.data_list({
                "Gateway Node": "us-east-edge-1",
                "Cert Expiration": "180 days remaining",
                "Firewall Rules": "32 enforced",
            }),
            title="Infrastructure Config",
            action=ui.button("Edit Config", variant="ghost"),
        ),
        gap="2rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
