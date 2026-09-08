import pylage as pl
"""Manual demo for PyLage pl.navigation & Wayfinding components (pl.menu, pl.breadcrumb_trail, pl.pagination, pl.navigation)."""



def get_app() -> pl.column:
    current_page = pl.state(1)
    active_nav_tab = pl.state("Overview")

    title = pl.heading("🧭 pl.navigation & Wayfinding Manual", level=1)
    desc = pl.text(
        "Demonstrates pl.navigation, pl.breadcrumb_trail, pl.pagination, and pl.menu components in PyLage.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # 1. pl.breadcrumb_trail Component
    crumbs_card = pl.card(
        pl.heading("1. Breadcrumb Trail", level=3),
        pl.text("Hierarchical path navigation with active current item:"),
        pl.breadcrumb_trail(
            items=["Home", "Workspaces", "Production Cluster", "App Settings"],
            style=pl.style(margin_top="0.75rem", font_size="0.875rem", color="#475569"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 2. pl.navigation & pl.menu
    nav_card = pl.card(
        pl.heading("2. Top pl.navigation Bar & Action pl.menu", level=3),
        pl.navigation(
            pl.row(
                pl.heading("⚡ PyLage Cloud", level=4, style=pl.style(margin=0, color="#1e293b")),
                pl.row(
                    pl.button("Dashboard", on_click=lambda: active_nav_tab.set("Dashboard")),
                    pl.button("Analytics", on_click=lambda: active_nav_tab.set("Analytics")),
                    pl.button("Settings", on_click=lambda: active_nav_tab.set("Settings")),
                    style=pl.style(gap="0.5rem"),
                ),
                style=pl.style(display="flex", justify_content="space-between", align_items="center", width="100%"),
            ),
            style=pl.style(
                background="#f8fafc",
                padding="0.75rem 1rem",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_top="0.75rem",
            ),
        ),
        pl.row(
            pl.text("Active Selected View: "),
            pl.badge(active_nav_tab, variant="primary"),
            style=pl.style(align_items="center", gap="0.5rem", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 3. pl.pagination Component
    def handle_page_change(e):
        page = int(e.get("page", 1))
        current_page.set(page)

    page_card = pl.card(
        pl.heading("3. Reactive pl.pagination", level=3),
        pl.row(
            pl.text("Current Active Page: "),
            pl.badge(current_page, variant="secondary"),
            style=pl.style(align_items="center", gap="0.5rem", margin_bottom="0.75rem"),
        ),
        pl.pagination(
            total_pages=10,
            current_page=current_page,
            on_page_change=handle_page_change,
            style=pl.style(margin_top="0.5rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        crumbs_card,
        nav_card,
        page_card,
        style=pl.style(padding="2rem", max_width="900px", margin="0 auto"),
    )
