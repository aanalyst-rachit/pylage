import pylage as pl
import pylage as ps
import pylage as ui

def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Empty State", level=2),
        pl.text("High-level empty state placeholders for dashboards, tables, and lists."),
        pl.grid(
            ui.empty_state(
                title="No notifications",
                description="You're all caught up! There are no unread notifications.",
                icon="🔔",
            ),
            ui.empty_state(
                title="No projects found",
                description="Get started by creating your first workspace project.",
                icon="📁",
                action=ui.button("New Project", variant="primary"),
            ),
            ui.empty_state(
                title="Search yielded no results",
                description="Try refining your query or resetting active search filters.",
                icon="🔍",
                action=ui.button("Clear filters", variant="outline"),
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
