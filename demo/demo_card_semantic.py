import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    click_count = pl.state(0)

    def mark_clicked():
        click_count.set(click_count.value + 1)

    return pl.column(
        pl.heading("PyLage UI Kit — Card", level=2),
        pl.text("Semantic Card API using the existing PyLage engine."),
        
        # Grid div par direct inline grid styles pass karein
        pl.grid(
            ui.card(
                heading="Revenue",
                body="₹42,000",
                footer="Monthly revenue",
            ),
            ui.card(
                heading="Active Users",
                body="12,450",
                footer="Growing steadily",
                variant="elevated",
            ),
            ui.card(
                heading="Orders",
                body="1,284",
                footer="Updated just now",
                variant="outlined",
            ),
            ui.card(
                heading="Interactive Card",
                body="Click to test state update",
                footer=click_count,
                variant="interactive",
                on_click=mark_clicked,
            ),
            style=pl.style(
                display="grid",
                grid_template_columns="repeat(auto-fit, minmax(280px, 1fr))",
                gap="1.5rem",
                width="100%"
            )
        ),
        gap="1.5rem",
        style=pl.style(max_width="1200px", margin="0 auto", padding="2rem")
    )