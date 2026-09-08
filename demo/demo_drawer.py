import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    drawer_open = pl.state(False)
    status_msg = pl.state("pl.drawer is currently closed.")

    def open_drawer(e=None):
        drawer_open.set(True)
        status_msg.set("pl.drawer is OPEN.")

    def close_drawer(e=None):
        drawer_open.set(False)
        status_msg.set("pl.drawer is CLOSED.")

    drawer_content = pl.column(
        pl.row(
            pl.heading("Navigation pl.drawer", level=3),
            pl.button("✕ Close", on_click=close_drawer, variant="secondary"),
            style=pl.style(display="flex", justify_content="space-between", align_items="center")
        ),
        pl.text("Navigation Links:"),
        pl.button("📊 Dashboard Overview", on_click=close_drawer),
        pl.button("👥 User Management", on_click=close_drawer),
        pl.button("⚙️ System Settings", on_click=close_drawer),
        pl.button("🔒 Security Audit", on_click=close_drawer),
        style=pl.style(padding="1.5rem", gap="1rem", width="280px", background="#ffffff", height="100%")
    )

    drawer_component = pl.drawer(
        drawer_content,
        open=drawer_open,
        title="Side Navigation pl.drawer",
        class_name="pylage-side-drawer"
    )

    app = pl.column(
        pl.heading("pl.drawer Component — Live Manual Test Suite", level=1),
        pl.text("Test side overlay drawer rendering, open state toggling, and close handlers."),
        pl.card(
            pl.row(
                pl.text("Current pl.State: ", style=pl.style(font_weight="bold")),
                pl.text(status_msg, style=pl.style(color="#2563eb", font_weight="bold")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        pl.button("Open Side pl.drawer", on_click=open_drawer, variant="primary"),
        drawer_component,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.drawer Manual Test", serve=True, host="0.0.0.0", port=3000)
