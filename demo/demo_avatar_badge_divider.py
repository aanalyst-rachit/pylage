import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    user_status = pl.State("Online")
    notif_count = pl.State(3)

    def toggle_status(e=None):
        if user_status.value == "Online":
            user_status.set("Away")
        else:
            user_status.set("Online")

    def increment_notifs(e=None):
        notif_count.set(notif_count.value + 1)

    # pl.avatar with pl.badge
    user_avatar = pl.avatar(
        pl.text("RK"),
        style=pl.style(
            display="inline-flex",
            align_items="center",
            justify_content="center",
            width="48px",
            height="48px",
            background="#3b82f6",
            color="#ffffff",
            font_weight="bold",
            border_radius="9999px",
            font_size="1.25rem"
        )
    )

    status_badge = pl.badge(
        user_status,
        style=pl.style(
            padding="0.25rem 0.5rem",
            background="#dcfce7",
            color="#15803d",
            font_size="0.75rem",
            font_weight="bold",
            border_radius="9999px"
        )
    )

    notif_badge = pl.badge(
        notif_count,
        style=pl.style(
            padding="0.25rem 0.5rem",
            background="#fee2e2",
            color="#b91c1c",
            font_size="0.75rem",
            font_weight="bold",
            border_radius="9999px"
        )
    )

    app = pl.column(
        pl.heading("pl.avatar, pl.badge, pl.divider & Canvas — Live Manual Test Suite", level=1),
        pl.text("Test visual utility components, reactive badges, dividers and canvas rendering."),
        pl.card(
            pl.row(
                user_avatar,
                pl.column(
                    pl.row(
                        pl.heading("Rachit Kanaujia", level=3, style=pl.style(margin="0")),
                        status_badge,
                        style=pl.style(display="flex", align_items="center", gap="0.75rem")
                    ),
                    pl.row(
                        pl.text("Unread Notifications: "),
                        notif_badge,
                        style=pl.style(display="flex", align_items="center", gap="0.5rem")
                    ),
                    style=pl.style(gap="0.25rem")
                ),
                style=pl.style(display="flex", align_items="center", gap="1.25rem")
            ),
            style=pl.style(padding="1.5rem", background="#f8fafc", border_radius="12px", margin_bottom="1rem")
        ),
        pl.divider(style=pl.style(margin="1.5rem 0", border_top="1px solid #e2e8f0")),
        pl.row(
            pl.button("Toggle Online/Away Status", on_click=toggle_status, variant="secondary"),
            pl.button("Add Notification (+1)", on_click=increment_notifs, variant="primary"),
            style=pl.style(display="flex", gap="1rem")
        ),
        pl.divider(style=pl.style(margin="1.5rem 0", border_top="1px solid #e2e8f0")),
        pl.heading("Canvas Element Integration", level=3),
        pl.Canvas(width=400, height=150, style=pl.style(border="1px dashed #94a3b8", border_radius="8px")),
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage pl.avatar/pl.badge/pl.divider Manual Test", serve=True, host="0.0.0.0", port=3000)
