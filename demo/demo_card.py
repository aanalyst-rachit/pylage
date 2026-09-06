import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps

def get_app():
    # Dynamic States for Interactivity
    click_count = pl.State(0)
    card_status = pl.State("Status: Idle")

    def handle_card_click():
        new_count = click_count.value + 1
        click_count.set(new_count)
        card_status.set(f"⚡ Interactive pl.card Clicked! Total: {new_count}")

    # ============================================================
    # 1. BASIC CARD
    # ============================================================
    basic_card = pl.card(
        pl.text("Minimal pl.card", style=pl.style(font_weight="700")),
        pl.text("Ye simple content container card hai.", style=pl.style(color="#64748b")),
        style=pl.style(
            background_color="#ffffff",
            padding="1.25rem",
            border_radius="0.5rem",
            border="1px solid #e2e8f0",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 2. ELEVATED CARD (Shadow & Custom Border)
    # ============================================================
    elevated_card = pl.card(
        pl.heading("Elevated pl.card", style=pl.style(font_size="1.25rem", color="#0f172a")),
        pl.text(
            "Box-shadow, custom border aur rounded corners prop customisation.",
            style=pl.style(color="#475569", margin_top="0.5rem"),
        ),
        style=pl.style(
            background_color="#ffffff",
            padding="1.5rem",
            border_radius="1rem",
            box_shadow="0 10px 15px -3px rgba(0, 0, 0, 0.1)",
            border="1px solid #cbd5e1",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 3. INTERACTIVE / CLICKABLE CARD
    # ============================================================
    interactive_card = pl.card(
        pl.heading("Interactive pl.card (Click Me)", style=pl.style(font_size="1.25rem", color="#2563eb")),
        pl.text("Click handling & dynamic state update demo.", style=pl.style(color="#64748b", margin_top="0.25rem")),
        pl.heading(click_count, style=pl.style(color="#166534", margin_top="1rem")),
        on_click=handle_card_click,
        style=pl.style(
            background_color="#eff6ff",
            padding="1.5rem",
            border_radius="0.75rem",
            border="2px dashed #2563eb",
            cursor="pointer",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 4. FULL COMPOSED CARD (Header, Body, Footer)
    # ============================================================
    composed_card = pl.card(
        # pl.card Header
        pl.column(
            pl.heading("Product Analytics", style=pl.style(font_size="1.25rem", color="#0f172a")),
            pl.text("Monthly subscription overview", style=pl.style(color="#64748b", font_size="0.875rem")),
            style=pl.style(margin_bottom="1rem"),
        ),
        # pl.card Body (Fixed pl.style without border_top/border_bottom)
        pl.column(
            pl.text("Active Users: 1,240", style=pl.style(font_weight="600", color="#166534")),
            pl.text("Revenue: $4,500", style=pl.style(font_weight="600", color="#2563eb")),
            style=pl.style(
                padding="1rem 0",
                border="1px solid #e2e8f0"
            ),
        ),
        # pl.card Footer Action
        pl.button(
            "View Full Report",
            style=pl.style(
                background_color="#0f172a",
                color="#ffffff",
                padding="0.5rem 1rem",
                border_radius="0.375rem",
                margin_top="1rem",
                cursor="pointer",
            ),
        ),
        style=pl.style(
            background_color="#ffffff",
            padding="1.5rem",
            border_radius="0.75rem",
            border="1px solid #e2e8f0",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
            margin_bottom="1.5rem",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage pl.card — Live Manual",
            style=pl.style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        pl.text(
            "pl.card component ke alag-alag variations aur interactive event handling test karein:",
            style=pl.style(color="#64748b", margin_bottom="1.5rem"),
        ),

        pl.text(card_status, style=pl.style(color="#166534", font_weight="600", margin_bottom="1rem")),

        pl.text("1. Basic pl.card", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        basic_card,

        pl.text("2. Elevated pl.card", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        elevated_card,

        pl.text("3. Interactive pl.card", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        interactive_card,

        pl.text("4. Composed pl.card", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        composed_card,

        style=pl.style(
            width="100%",
            max_width="700px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )
