import pylage as pl
"""Manual demo for PyLage Layout Primitives (AppShell, Center, Stack, Split, TwoColumn, ThreeColumn, SidebarLayout)."""



def get_app() -> pl.column:
    title = pl.heading("🏗️ Layout Primitives Manual", level=1)
    desc = pl.text(
        "Demonstrates foundational layout primitives and responsive structural containers.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # 1. AppShell Layout
    shell_demo = pl.card(
        pl.heading("1. AppShell Layout Structure", level=3),
        pl.text("Composed Header, Sidebar, and Content with responsive flow:"),
        pl.app_shell(
            header=pl.navbar(pl.heading("App Header", level=4), pl.button("Logout")),
            sidebar=pl.column(pl.text("📁 Nav Item 1"), pl.text("⚙️ Nav Item 2"), style=pl.style(width="200px", padding="1rem", background="#f1f5f9")),
            content=pl.column(pl.heading("Main View Content", level=3), pl.text("Fluid responsive content zone."), style=pl.style(padding="1rem")),
            footer=pl.footer(pl.text("© 2026 PyLage Layout Primitives. All rights reserved.")),
            style=pl.style(border="1px solid #cbd5e1", border_radius="0.5rem", overflow="hidden", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 2. Split, TwoColumn, and ThreeColumn
    multi_col_demo = pl.card(
        pl.heading("2. Multi-pl.column Grid Primitives", level=3),
        pl.text("TwoColumn and ThreeColumn responsive containers:"),
        pl.two_column(
            pl.card(pl.heading("Left pl.column", level=4), pl.text("50% split on desktop, stacked on mobile.")),
            pl.card(pl.heading("Right pl.column", level=4), pl.text("50% split on desktop, stacked on mobile.")),
            style=pl.style(margin_top="0.75rem", margin_bottom="1rem"),
        ),
        pl.three_column(
            pl.card(pl.heading("pl.column A", level=4), pl.text("1/3 width")),
            pl.card(pl.heading("pl.column B", level=4), pl.text("1/3 width")),
            pl.card(pl.heading("pl.column C", level=4), pl.text("1/3 width")),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 3. Center Primitive
    center_demo = pl.card(
        pl.heading("3. Center Alignment Container", level=3),
        pl.center(
            pl.card(
                pl.heading("Centered Dialog / Modal Box", level=4),
                pl.text("Horizontally and vertically centered inside the parent container."),
                pl.button("Confirm Action", style=pl.style(margin_top="0.5rem")),
                style=pl.style(padding="1.5rem", text_align="center", background="#f8fafc", border="1px solid #cbd5e1", border_radius="0.5rem"),
            ),
            style=pl.style(min_height="180px", background="#f1f5f9", border_radius="0.5rem", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        shell_demo,
        multi_col_demo,
        center_demo,
        style=pl.style(padding="2rem", max_width="1000px", margin="0 auto"),
    )
