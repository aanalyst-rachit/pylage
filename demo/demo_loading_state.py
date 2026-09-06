import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Loading State", level=2),
        pl.text("High-level feedback spinners and loaders for async workflows."),
        pl.grid(
            ui.loading_state(
                text="Loading dashboard...",
                description="Fetching latest analytics from the cluster.",
            ),
            ui.loading_state(
                text="Importing dataset",
                description="Parsing CSV and computing summary metrics.",
            ),
            ui.loading_state(
                text="Synchronizing state",
                spinner=True,
            ),
            style=pl.style(
                display="grid",
                grid_template_columns="repeat(auto-fit, minmax(300px, 1fr))",
                gap="1.5rem",
                width="100%",
            ),
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
