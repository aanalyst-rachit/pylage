import pylage as pl


label = "Settings"


def page():
    return pl.column(
        pl.heading("Settings", level=2),
        pl.text("Navigation from pl.navigation_item() reached /settings."),
        style=pl.style(
            gap="0.75rem",
            padding="1.5rem",
        ),
    )
