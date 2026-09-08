import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    dialog_open = pl.state(False)
    action_log = pl.state("No dialog action taken yet.")

    def open_dialog(e=None):
        dialog_open.set(True)
        action_log.set("pl.dialog opened by user.")

    def confirm_action(e=None):
        dialog_open.set(False)
        action_log.set("pl.dialog confirmed & closed.")

    def cancel_action(e=None):
        dialog_open.set(False)
        action_log.set("pl.dialog cancelled & closed.")

    dialog_modal = pl.dialog(
        pl.card(
            pl.heading("Confirm System Deployment", level=3),
            pl.text("Are you sure you want to deploy the updated PyLage components to production?"),
            pl.row(
                pl.button("Cancel", on_click=cancel_action, variant="secondary"),
                pl.button("Confirm & Deploy", on_click=confirm_action, variant="primary"),
                style=pl.style(display="flex", justify_content="flex-end", gap="0.75rem", margin_top="1.5rem")
            ),
            style=pl.style(padding="1.5rem", background="#ffffff", border_radius="12px", max_width="450px")
        ),
        open=dialog_open,
        title="Deployment Modal pl.dialog",
        class_name="pylage-dialog-overlay"
    )

    app = pl.column(
        pl.heading("pl.dialog / Modal Component — Live Manual Test Suite", level=1),
        pl.text("Test dialog backdrop rendering, open/close boolean state toggling, and nested actions."),
        pl.card(
            pl.row(
                pl.text("pl.dialog Status: ", style=pl.style(font_weight="bold")),
                pl.text(action_log, style=pl.style(color="#2563eb", font_weight="bold")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        pl.button("Open Modal pl.dialog", on_click=open_dialog, variant="primary"),
        dialog_modal,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.dialog Manual Test", serve=True, host="0.0.0.0", port=3000)
