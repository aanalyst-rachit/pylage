import pylage as pl


label = "Projects"


def page():
    return pl.column(
        pl.heading("Projects", level=2),
        pl.text("Navigation from pl.navigation_item() reached /projects."),
        style=pl.style(
            gap="0.75rem",
            padding="1.5rem",
        ),
    )
