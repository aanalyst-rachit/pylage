import pylage as pl


NAV_CONTAINER_STYLE = pl.style(
    display="flex",
    flex_direction="column",
    gap="0.5rem",
    width="100%",
)


def dashboard_page():
    return pl.column(
        pl.dashboard_header(
            "Executive Operations Control",
            "High-level platform monitoring, usage telemetry, and customer accounts.",
            actions=[
                pl.button("Generate Audit", variant="outline"),
                pl.button("Deployment Console", variant="primary"),
            ],
        ),
        # Metrics Row
        pl.column(
            pl.metric_grid(
                pl.metric(
                    label="Global Revenue",
                    value="₹42,80,000",
                    delta="+18.4%",
                    description="vs last month",
                ),
                pl.metric(
                    label="Total Workspaces",
                    value="1,240",
                    delta="+42",
                    description="Active clusters",
                ),
                pl.metric(
                    label="Fleet Availability",
                    value="99.99%",
                    delta="0.0%",
                    description="All regions green",
                ),
                columns=3,
            ),
            style=pl.style(margin_bottom="1rem"),
        ),
        # Resources Row
        pl.column(
            pl.dashboard_grid(
                pl.dashboard_card(
                    title="Resource Allocation",
                    body="Compute and edge nodes are operating at balanced capacity with auto-scaling enabled.",
                    action=pl.badge("Optimized", variant="success"),
                    footer="Node count: 128 instances",
                ),
                pl.dashboard_card(
                    title="Service Gateways",
                    body="All ingress traffic load balancers are passing edge validation with zero timeouts.",
                    action=pl.badge("Healthy", variant="success"),
                    footer="Latency: 18ms p95",
                ),
                layout="2-col",
            ),
            style=pl.style(margin_bottom="1.5rem"),
        ),
        # Table Row
        pl.card(
            pl.heading("Cluster Health", level=3),
            pl.table(
                [
                    ["Cluster Alpha", "Mumbai", "100%", "Healthy"],
                    ["Cluster Beta", "Bengaluru", "98.8%", "Healthy"],
                    ["Cluster Gamma", "Delhi", "99.4%", "Healthy"],
                ],
                headers=["Cluster", "Region", "SLA", "Status"],
            ),
        ),
        # Footer Row
        pl.card(
            pl.text(
                "PyLage Operations Console — Phase 18 Example Application"
            ),
        ),
    )


def analytics_page():
    return pl.column(
        pl.dashboard_header(
            "Analytics",
            "Platform performance, growth and operational trends.",
        ),
        pl.column(
            pl.metric_grid(
                pl.metric(label="Requests / sec", value="89.2K", delta="+8.1%"),
                pl.metric(label="P99 Latency", value="4.2ms", delta="-18.5%"),
                pl.metric(label="Active Seats", value="18,400", delta="+850"),
                columns=3,
            ),
            style=pl.style(margin_bottom="1.5rem"),
        ),
        pl.column(
            pl.dashboard_grid(
                pl.dashboard_card(
                    title="Revenue Trend",
                    body=pl.column(
                        pl.trend("+18.4%", direction="up"),
                        pl.text("Monthly recurring revenue continues to grow."),
                        gap="0.5rem",
                    ),
                    action=pl.badge("Positive", variant="success"),
                ),
                pl.dashboard_card(
                    title="Latency Trend",
                    body=pl.column(
                        pl.trend("-18.5%", direction="down"),
                        pl.text(
                            "Lower latency indicates improved platform performance."
                        ),
                        gap="0.5rem",
                    ),
                    action=pl.badge("Improving", variant="success"),
                ),
                layout="2-col",
            ),
            style=pl.style(margin_bottom="1.5rem"),
        ),
        pl.card(
            pl.heading("Analytics Summary", level=3),
            pl.table(
                [
                    ["Revenue", "₹42.8L", "+18.4%", "Positive"],
                    ["Requests", "89.2K/s", "+8.1%", "Positive"],
                    ["Latency", "4.2ms", "-18.5%", "Improving"],
                ],
                headers=["Metric", "Current", "Change", "Signal"],
            ),
        ),
    )


def forms_page():
    submitted = pl.State("No submission yet.")

    def handle_submit(payload=None):
        values = payload.get("values", {}) if isinstance(payload, dict) else {}
        submitted.set(f"{values.get('name', '')} · {values.get('email', '')}")

    return pl.column(
        pl.dashboard_header(
            "Forms", "Manage workspace and account information."
        ),
        pl.card(
            pl.form(
                pl.form_field(
                    pl.input(
                        value="Rachit", name="name", placeholder="Your name"
                    ),
                    label="Name",
                    required=True,
                ),
                pl.form_field(
                    pl.input(
                        value="rachit@example.com",
                        name="email",
                        input_type="email",
                        placeholder="Email",
                    ),
                    label="Email",
                    required=True,
                ),
                pl.form_field(
                    pl.checkbox(checked=False, name="terms"),
                    label="Accept terms",
                ),
                pl.button("Save Changes", type="submit", variant="primary"),
                pl.text("Latest submission:"),
                pl.text(submitted),
                on_submit=handle_submit,
                method="post",
                action="/submit",
                style=pl.style(
                    display="flex", flex_direction="column", gap="1rem"
                ),
            ),
        ),
    )


def tables_page():
    current_page = pl.State(1)

    def change_page(payload=None):
        if isinstance(payload, dict):
            current_page.set(int(payload.get("page", 1)))

    return pl.column(
        pl.dashboard_header(
            "Tables", "Operational clusters and service status."
        ),
        pl.card(
            pl.table(
                [
                    ["1001", "Alpha", "Mumbai", "Healthy"],
                    ["1002", "Beta", "Bengaluru", "Healthy"],
                    ["1003", "Gamma", "Delhi", "Warning"],
                    ["1004", "Delta", "Hyderabad", "Healthy"],
                ],
                headers=["ID", "Cluster", "Region", "Status"],
            ),
            pl.row(
                pl.text("Current page:"),
                pl.badge(str(current_page.value), variant="secondary"),
                align_items="center",
                gap="0.5rem",
            ),
            pl.pagination(
                total_pages=5,
                current_page=current_page,
                on_page_change=change_page,
            ),
        ),
    )


def navigation_page():
    return pl.column(
        pl.dashboard_header(
            "Navigation",
            "Application navigation patterns powered by the UI Kit.",
        ),
        pl.card(
            pl.heading("Workspace Navigation", level=3),
            pl.navigation(
                pl.navigation_item("Overview", active=True),
                pl.navigation_item("Projects"),
                pl.navigation_item("Team"),
                pl.navigation_item("Settings"),
            ),
        ),
    )


def overlays_page():
    drawer_open = pl.State(False)
    modal_open = pl.State(False)
    toast_visible = pl.State(False)

    drawer = pl.drawer(
        pl.column(
            pl.heading("Quick Actions", level=3),
            pl.text("Off-canvas application controls."),
            pl.button(
                "Close Drawer", on_click=lambda: drawer_open.set(False)
            ),
            gap="1rem",
        ),
        open=drawer_open,
        title="Quick Actions",
    )
    modal = pl.modal(
        pl.column(
            pl.text("Confirm this application action?"),
            pl.button(
                "Confirm",
                on_click=lambda: modal_open.set(False),
                variant="primary",
            ),
            gap="1rem",
        ),
        open=modal_open,
        title="Confirm Action",
    )

    return pl.column(
        pl.dashboard_header(
            "Overlays", "Drawer, modal and toast interaction examples."
        ),
        pl.card(
            pl.row(
                pl.button(
                    "Open Drawer",
                    on_click=lambda: drawer_open.set(True),
                    variant="primary",
                ),
                pl.button("Open Modal", on_click=lambda: modal_open.set(True)),
                pl.button(
                    "Show Toast", on_click=lambda: toast_visible.set(True)
                ),
                gap="0.75rem",
            ),
            pl.toast(
                "Action completed successfully.",
                visible=toast_visible,
                variant="success",
            ),
            drawer,
            modal,
        ),
    )


def components_page():
    return pl.column(
        pl.dashboard_header(
            "Components",
            "Reusable UI Kit primitives composed into product surfaces.",
        ),
        pl.column(
            pl.dashboard_grid(
                pl.dashboard_card(
                    title="Status",
                    body=pl.column(
                        pl.badge("Production", variant="success"),
                        pl.text("All core services are operational."),
                        gap="0.5rem",
                    ),
                ),
                pl.dashboard_card(
                    title="Notice",
                    body=pl.alert(
                        "Scheduled maintenance tonight.", type="info"
                    ),
                ),
                layout="2-col",
            ),
            style=pl.style(margin_bottom="1.5rem"),
        ),
        pl.card(
            pl.heading("Actions", level=3),
            pl.row(
                pl.button("Primary Action", variant="primary"),
                pl.button("Secondary Action", variant="secondary"),
                pl.button("Outlined Action", variant="outline"),
                gap="0.75rem",
            ),
        ),
    )


def themes_page():
    return pl.column(
        pl.dashboard_header(
            "Themes",
            "Use the public PyLage theme API to switch application appearance.",
        ),
        pl.card(
            pl.heading("Theme Controls", level=3),
            pl.row(
                pl.button(
                    "Light Theme", on_click=lambda: pl.set_theme("light")
                ),
                pl.button("Dark Theme", on_click=lambda: pl.set_theme("dark")),
                gap="0.75rem",
            ),
            pl.text("Theme switching uses pl.set_theme()."),
        ),
    )


PAGES = {
    "Dashboard": dashboard_page,
    "Analytics": analytics_page,
    "Forms": forms_page,
    "Tables": tables_page,
    "Navigation": navigation_page,
    "Overlays": overlays_page,
    "Components": components_page,
    "Themes": themes_page,
}


def get_app():
    active_page = pl.State("Dashboard")
    content = pl.column(dashboard_page())

    def select_page(name):
        def handler(payload=None):
            active_page.set(name)
            content.set_children(PAGES[name]())

        return handler

    # Fixed: Removed hardcoded background_color and border to allow theme dynamic rendering
    sidebar = pl.column(
        pl.column(
            pl.heading("PyLage", level=2),
            pl.text("UI Kit"),
            style=pl.style(margin_bottom="1.25rem"),
        ),
        pl.navigation(
            *[
                pl.navigation_item(
                    name,
                    active=(active_page.value == name),  # Dynamic boolean check
                    on_click=select_page(name),
                    style=pl.style(margin_bottom="0.375rem"),
                )
                for name in PAGES
            ],
            style=NAV_CONTAINER_STYLE,
        ),
        style=pl.style(
            width="240px",
            min_width="240px",
            padding="1.5rem",
            box_sizing="border-box",
        ),
    )

    header = pl.dashboard_header(
        "PyLage UI Kit",
        "Phase 18 — Example Application",
        actions=[pl.badge("Production Demo", variant="success")],
    )

    return pl.dashboard(
        header=header,
        sidebar=sidebar,
        content=content,
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage UI Kit — Example Application",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )