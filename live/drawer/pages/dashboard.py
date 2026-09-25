import pylage as pl


label = "Dashboard"


def page():
    return pl.column(
        pl.heading("Dashboard", level=2),
        pl.text("Navigation from pl.navigation_item() reached /dashboard."),
        style=pl.style(
            gap="0.75rem",
            padding="1.5rem",
        ),
    )
