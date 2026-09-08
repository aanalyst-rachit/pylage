import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    active_tab = pl.state("tab_analytics")
    tab_title = pl.state("Analytics & Metrics")

    def switch_to_analytics(e=None):
        active_tab.set("tab_analytics")
        tab_title.set("Analytics & Metrics")

    def switch_to_security(e=None):
        active_tab.set("tab_security")
        tab_title.set("Security & Permissions")

    def switch_to_billing(e=None):
        active_tab.set("tab_billing")
        tab_title.set("Billing & Plans")

    # Tab switcher navigation bar
    nav_tabs = pl.row(
        pl.button("Analytics", on_click=switch_to_analytics, variant="primary"),
        pl.button("Security", on_click=switch_to_security, variant="secondary"),
        pl.button("Billing", on_click=switch_to_billing, variant="secondary"),
        style=pl.style(display="flex", gap="0.5rem", border_bottom="1px solid #e2e8f0", padding_bottom="0.5rem")
    )

    tab_container = pl.tabs(
        nav_tabs,
        class_name="pylage-tabs-container",
        title="PyLage Reactive pl.tabs",
        style=pl.style(width="100%", max_width="700px")
    )

    app = pl.column(
        pl.heading("pl.tabs Component — Live Manual Test Suite", level=1),
        pl.text("Test active tab state synchronization, tab switching callbacks, and panel displays."),
        pl.card(
            pl.row(
                pl.text("Currently Active View: ", style=pl.style(font_weight="bold")),
                pl.heading(tab_title, level=3, style=pl.style(color="#2563eb", margin="0")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        tab_container,
        pl.card(
            pl.heading(tab_title, level=4),
            pl.text("Content dynamically synchronized with the selected active tab state."),
            style=pl.style(padding="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="8px", margin_top="1rem")
        ),
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.tabs Manual Test", serve=True, host="0.0.0.0", port=3000)
