import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Error State", level=2),
        pl.text("High-level error boundary and failure feedback cards."),
        pl.grid(
            ui.error_state(
                title="Failed to fetch data",
                description="The remote server returned a 500 Internal Server Error.",
                icon="⚠️",
                action=ui.button("Retry connection", variant="danger"),
            ),
            ui.error_state(
                title="Authentication required",
                description="Your session has expired. Please sign in again to continue.",
                icon="🔒",
                action=ui.button("Sign In", variant="primary"),
            ),
            ui.error_state(
                title="Invalid file format",
                description="Only .csv and .parquet files are supported by this importer.",
                icon="🚫",
            ),
            style=pl.style(
                display="grid",
                grid_template_columns="repeat(auto-fit, minmax(320px, 1fr))",
                gap="1.5rem",
                width="100%",
            ),
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem"),
    )
