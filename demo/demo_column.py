import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps

def get_app():
    # Dynamic pl.State for pl.column Interactivity Demo
    item_count = pl.state(2)

    def add_item():
        item_count.set(item_count.value + 1)

    def reset_items():
        item_count.set(2)

    # Helper function for dynamic item blocks
    def create_block(text, bg_color="#2563eb", width="100%"):
        return pl.column(
            pl.text(text, style=pl.style(color="#ffffff", font_weight="700")),
            style=pl.style(
                background_color=bg_color,
                width=width,
                padding="0.75rem 1rem",
                border_radius="0.375rem",
            ),
        )

    # ============================================================
    # 1. BASIC COLUMN WITH GAP
    # ============================================================
    basic_column = pl.column(
        create_block("Stacked Block 1", "#2563eb"),
        create_block("Stacked Block 2", "#7c3aed"),
        create_block("Stacked Block 3", "#dc2626"),
        style=pl.style(
            gap="0.75rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 2. ALIGN ITEMS (Horizontal Alignment in Vertical pl.column)
    # ============================================================
    align_column = pl.column(
        create_block("Start Aligned", "#059669", width="40%"),
        create_block("Center Aligned", "#d97706", width="50%"),
        create_block("End Aligned", "#2563eb", width="40%"),
        style=pl.style(
            align_items="center",  # Centers all child blocks horizontally
            gap="0.75rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 3. JUSTIFY CONTENT (Vertical Distribution inside Fixed Height)
    # ============================================================
    justify_column = pl.column(
        create_block("Top Block", "#7c3aed"),
        create_block("Bottom Block", "#059669"),
        style=pl.style(
            justify_content="space-between",
            height="180px",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 4. SCROLLABLE COLUMN CONTAINER
    # ============================================================
    scroll_column = pl.column(
        create_block("Scrollable Item 1", "#475569"),
        create_block("Scrollable Item 2", "#475569"),
        create_block("Scrollable Item 3", "#475569"),
        create_block("Scrollable Item 4", "#475569"),
        create_block("Scrollable Item 5", "#475569"),
        style=pl.style(
            gap="0.5rem",
            height="140px",
            overflow="auto",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 5. INTERACTIVE COLUMN (Dynamic Content Stacking)
    # ============================================================
    interactive_column = pl.column(
        pl.row(
            pl.button("Add Stack Item", on_click=add_item, style=pl.style(padding="0.5rem 1rem", cursor="pointer")),
            pl.button("Reset", on_click=reset_items, style=pl.style(padding="0.5rem 1rem", cursor="pointer")),
            style=pl.style(gap="0.75rem", margin_bottom="1rem"),
        ),
        pl.row(
            pl.text("Current Items Stacked: ", style=pl.style(font_weight="600")),
            pl.heading(item_count, style=pl.style(color="#2563eb", font_size="1rem")),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),
        style=pl.style(
            gap="0.5rem",
            padding="1rem",
            background_color="#eff6ff",
            border="1px dashed #2563eb",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage pl.column — Live Manual",
            style=pl.style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        pl.text(
            "pl.column layout component ke vertical stacking, alignment, aur scrollable features test karein:",
            style=pl.style(color="#64748b", margin_bottom="1.5rem"),
        ),

        pl.text("1. Basic Vertical Stacking (With Gap)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        basic_column,

        pl.text("2. Horizontal Alignment (Align Items Center)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        align_column,

        pl.text("3. Vertical Distribution (Justify Space-Between)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        justify_column,

        pl.text("4. Fixed Height Scrollable pl.column", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        scroll_column,

        pl.text("5. Interactive pl.column pl.State Update", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        interactive_column,

        style=pl.style(
            width="100%",
            max_width="750px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )
