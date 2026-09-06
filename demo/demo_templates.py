import pylage as pl
"""Manual demo for PyLage Application Templates (Dashboard, Admin, Profile, Settings, Landing, Docs)."""



def get_app() -> pl.column:
    selected_template = pl.State("dashboard")

    title = pl.heading("📄 PyLage Application Templates Manual", level=1)
    desc = pl.text(
        "Demonstrates complete production application page templates provided by pylage_layout.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # Template selector buttons
    selector_row = pl.row(
        pl.button("Dashboard Template", on_click=lambda: selected_template.set("dashboard")),
        pl.button("Admin Console", on_click=lambda: selected_template.set("admin")),
        pl.button("Profile & Account", on_click=lambda: selected_template.set("profile")),
        pl.button("Documentation", on_click=lambda: selected_template.set("docs")),
        style=pl.style(gap="0.75rem", margin_bottom="1.5rem", flex_wrap="wrap"),
    )

    # Preview pl.card
    template_preview = pl.card(
        pl.heading("Dashboard Template Preview", level=3),
        pl.text("Full-featured analytics and monitoring dashboard layout:"),
        pl.dashboard(
            title="Real-time Metrics Dashboard",
            sidebar_items=["Analytics", "Servers", "Databases", "Logs", "Alerts"],
            content=pl.column(
                pl.text("Enterprise cluster telemetry running at 99.99% availability."),
                style=pl.style(padding="1rem"),
            ),
        ),
        style=pl.style(padding="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        selector_row,
        template_preview,
        style=pl.style(padding="2rem", max_width="1000px", margin="0 auto"),
    )
