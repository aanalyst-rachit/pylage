import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    menu_selection = pl.state("None")
    tooltip_hits = pl.state(0)

    def select_item(name):
        def handler(e=None):
            menu_selection.set(name)
        return handler

    def increment_tooltip(e=None):
        tooltip_hits.set(tooltip_hits.value + 1)

    # pl.tooltip Demo
    tip_button = pl.button(
        "Hover or Click pl.tooltip Trigger",
        on_click=increment_tooltip,
        variant="primary"
    )
    tooltip_component = pl.tooltip(
        tip_button,
        pl.text("🚀 PyLage High-Performance pl.tooltip: Zero Client Bundles!"),
        title="Quick Info pl.tooltip"
    )

    # pl.menu Demo
    menu_items = pl.column(
        pl.button("Profile Settings", on_click=select_item("Profile Settings")),
        pl.button("API Tokens", on_click=select_item("API Tokens")),
        pl.button("Logout Session", on_click=select_item("Logout Session")),
        style=pl.style(display="flex", gap="0.5rem", padding="0.75rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="8px")
    )
    menu_component = pl.menu(
        menu_items,
        title="User Action pl.menu",
        class_name="pylage-action-menu"
    )

    # pl.popover Demo
    popover_content = pl.card(
        pl.heading("Quick Stats pl.popover", level=4),
        pl.text("Memory: 18.2 MB | Active Sockets: 1"),
        style=pl.style(padding="1rem", background="#f1f5f9", border_radius="6px")
    )
    popover_component = pl.popover(
        popover_content,
        title="Server Diagnostics",
        class_name="pylage-popover-panel"
    )

    app = pl.column(
        pl.heading("pl.popover, pl.tooltip & pl.menu — Live Manual Test Suite", level=1),
        pl.text("Test floating utility components, tooltips, interactive contextual menus and popovers."),
        pl.card(
            pl.row(
                pl.text("Selected pl.menu Option: ", style=pl.style(font_weight="bold")),
                pl.heading(menu_selection, level=3, style=pl.style(color="#2563eb", margin="0")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            pl.row(
                pl.text("pl.tooltip Trigger Interactions: ", style=pl.style(font_weight="bold")),
                pl.text(tooltip_hits, style=pl.style(color="#10b981", font_weight="bold")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        pl.heading("1. pl.tooltip Component", level=3),
        tooltip_component,
        pl.heading("2. Context pl.menu Component", level=3, style=pl.style(margin_top="1.5rem")),
        menu_component,
        pl.heading("3. pl.popover Component", level=3, style=pl.style(margin_top="1.5rem")),
        popover_component,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.popover/pl.tooltip/pl.menu Manual Test", serve=True, host="0.0.0.0", port=3000)
