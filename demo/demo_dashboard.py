import pylage as ui

def get_app():
    return ui.dashboard(
        header=ui.dashboard_header(
            title="Executive Operations Control",
            description="High-level fleet monitoring, usage telemetry, and customer accounts.",
            actions=[
                ui.button("Generate Audit", variant="outline"),
                ui.button("Deployment Console", variant="primary"),
            ],
        ),
        metrics=[
            ui.metric(label="Global Revenue", value="₹42,80,000", delta="+18.4%", description="vs last month"),
            ui.metric(label="Total Workspaces", value="1,240", delta="+42", description="Active clusters"),
            ui.metric(label="Fleet Availability", value="99.99%", delta="0.0%", description="All regions green"),
        ],
        content=ui.dashboard_grid(
            ui.dashboard_card(
                title="Resource Allocation",
                body="Compute and edge nodes are operating at balanced capacity with auto-scaling enabled.",
                action=ui.badge("Optimized", variant="success"),
                footer="Node count: 128 instances",
            ),
            ui.dashboard_card(
                title="Service Gateways",
                body="All ingress traffic load balancers passing edge validation checks with zero timeouts.",
                action=ui.badge("Healthy", variant="success"),
                footer="Latency: 18ms p95",
            ),
            layout="2-col",
        ),
        table=ui.table(
            [
                ["Cluster Alpha", "Mumbai", "100%", "Healthy"],
                ["Cluster Beta", "Bengaluru", "98.8%", "Healthy"],
                ["Cluster Gamma", "Delhi", "99.4%", "Healthy"],
            ],
            headers=["Cluster", "Region", "SLA", "Status"],
        ),
        footer=ui.card(
            body="PyLage Operations Console — Version 0.1.0 Production",
            variant="outlined",
        ),
    )
