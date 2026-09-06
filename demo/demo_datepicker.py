import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    selected_date = pl.State("2026-09-01")
    date_display = pl.State("2026-09-01")

    def handle_date_change(val=None):
        if isinstance(val, dict):
            val = val.get("value", selected_date.value)
        selected_date.set(str(val))
        date_display.set(str(val))

    def set_today(e=None):
        selected_date.set("2026-09-01")
        date_display.set("2026-09-01")

    def set_next_week(e=None):
        selected_date.set("2026-09-08")
        date_display.set("2026-09-08")

    picker = pl.datepicker(
        value=selected_date,
        on_change=handle_date_change,
        style=pl.style(padding="0.5rem 0.75rem", border="1px solid #cbd5e1", border_radius="6px", font_size="1rem")
    )

    quick_actions = pl.row(
        pl.button("Today", on_click=set_today, variant="secondary"),
        pl.button("+1 Week", on_click=set_next_week, variant="secondary"),
        style=pl.style(display="flex", gap="0.5rem", margin_top="0.75rem")
    )

    app = pl.column(
        pl.heading("pl.datepicker Component — Live Manual Test Suite", level=1),
        pl.text("Test bidirectional date binding, HTML5 date picker rendering, and programmatic state overrides."),
        pl.card(
            pl.row(
                pl.text("Selected Date Value: ", style=pl.style(font_weight="bold")),
                pl.heading(date_display, level=3, style=pl.style(color="#2563eb", margin="0")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        picker,
        quick_actions,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.datepicker Manual Test", serve=True, host="0.0.0.0", port=3000)
