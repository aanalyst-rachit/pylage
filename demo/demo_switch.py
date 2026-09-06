import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # -------------------------------------------------------------------------
    # pl.State Management
    # -------------------------------------------------------------------------
    dark_mode = pl.State(False)
    notifications_enabled = pl.State(False)

    # pl.State Inverter Handlers
    def toggle_dark_mode(val=None):
        dark_mode.set(not dark_mode.value)

    def toggle_notifications(val=None):
        notifications_enabled.set(not notifications_enabled.value)

    # Clean Safe pl.checkbox Constructor (Avoids duplicate 'type' parameter conflict)
    def create_checkbox(checked_val, click_handler):
        # 1. Preferred Native PyLage pl.checkbox Component
        if hasattr(ps, "pl.checkbox"):
            return pl.checkbox(
                value=checked_val,
                on_change=click_handler,
                style=pl.style(width="18px", height="18px", cursor="pointer")
            )

        # 2. Safe Fallback using generic PyLage Component engine
        from pylage.ENGINE.core.component import Component
        chk = Component("input")
        chk.props["type"] = "checkbox"
        chk.props["checked"] = checked_val
        chk.on("click", click_handler)
        chk.on("change", click_handler)
        return chk

    # -------------------------------------------------------------------------
    # UI Component Tree Return
    # -------------------------------------------------------------------------
    return pl.column(
        # Page Title
        pl.heading(
            "Switch Component Demo",
            style=pl.style(
                font_size="1.75rem",
                font_weight="800",
                color="#0f172a",
                margin_bottom="0.25rem",
            ),
        ),
        pl.text(
            "Interactive demonstration of toggle states in PyLage.",
            style=pl.style(color="#64748b", font_size="0.9rem", margin_bottom="1.5rem"),
        ),

        # ---------------------------------------------------------------------
        # DEMO 1: Dark Mode Toggle
        # ---------------------------------------------------------------------
        pl.column(
            pl.row(
                pl.text("Dark Theme: ", style=pl.style(font_weight="500", color="#475569")),
                pl.text(dark_mode, style=pl.style(color="#2563eb", font_weight="700")),
                style=pl.style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            pl.row(
                create_checkbox(dark_mode.value, toggle_dark_mode),
                pl.text("Enable Dark Theme", style=pl.style(color="#334155", font_size="0.95rem", cursor="pointer")),
                style=pl.style(gap="0.75rem", align_items="center"),
            ),
            style=pl.style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                margin_bottom="1rem",
                width="100%",
            ),
        ),

        # ---------------------------------------------------------------------
        # DEMO 2: Notifications Toggle
        # ---------------------------------------------------------------------
        pl.column(
            pl.row(
                pl.text("Notifications: ", style=pl.style(font_weight="500", color="#475569")),
                pl.text(notifications_enabled, style=pl.style(color="#059669", font_weight="700")),
                style=pl.style(gap="0.5rem", align_items="center", margin_bottom="0.75rem"),
            ),
            pl.row(
                create_checkbox(notifications_enabled.value, toggle_notifications),
                pl.text("Allow Email Notifications", style=pl.style(color="#334155", font_size="0.95rem", cursor="pointer")),
                style=pl.style(gap="0.75rem", align_items="center"),
            ),
            style=pl.style(
                padding="1rem",
                background_color="#ffffff",
                border="1px solid #e2e8f0",
                border_radius="0.5rem",
                width="100%",
            ),
        ),

        # Outer Layout Styling
        style=pl.style(
            width="100%",
            max_width="560px",
            padding="2rem",
            background_color="#f8fafc",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )
