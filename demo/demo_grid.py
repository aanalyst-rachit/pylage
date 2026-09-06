import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps

def get_app():
    # Dynamic pl.State for Grid Interactivity Demo
    selected_card = pl.State("None")

    def select_card_1():
        selected_card.set("Card 1 Selected")

    def select_card_2():
        selected_card.set("Card 2 Selected")

    def select_card_3():
        selected_card.set("Card 3 Selected")

    def select_card_4():
        selected_card.set("Card 4 Selected")

    # Helper function to generate grid items
    def create_grid_item(title, bg_color="#2563eb", height="80px"):
        return pl.column(
            pl.text(title, style=pl.style(color="#ffffff", font_weight="700")),
            style=pl.style(
                background_color=bg_color,
                height=height,
                display="flex",
                align_items="center",
                justify_content="center",
                border_radius="0.5rem",
            ),
        )

    # ============================================================
    # 1. EQUAL FIXED-COLUMN GRID (3 Columns)
    # ============================================================
    fixed_grid = pl.grid(
        create_grid_item("Item 1", "#2563eb"),
        create_grid_item("Item 2", "#7c3aed"),
        create_grid_item("Item 3", "#dc2626"),
        create_grid_item("Item 4", "#059669"),
        create_grid_item("Item 5", "#d97706"),
        create_grid_item("Item 6", "#0284c7"),
        style=pl.style(
            grid_template_columns="repeat(3, 1fr)",
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 2. ASYMMETRIC / CUSTOM TEMPLATE COLUMNS (Sidebar + Content)
    # ============================================================
    asymmetric_grid = pl.grid(
        create_grid_item("Sidebar (1fr)", "#475569", height="100px"),
        create_grid_item("Main Content (3fr)", "#2563eb", height="100px"),
        style=pl.style(
            grid_template_columns="1fr 3fr",
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 3. AUTO-FIT RESPONSIVE GRID
    # ============================================================
    responsive_grid = pl.grid(
        create_grid_item("Card A", "#059669"),
        create_grid_item("Card B", "#7c3aed"),
        create_grid_item("Card C", "#d97706"),
        create_grid_item("Card D", "#dc2626"),
        style=pl.style(
            grid_template_columns="repeat(auto-fit, minmax(140px, 1fr))",
            gap="1rem",
            padding="1rem",
            background_color="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    # ============================================================
    # 4. INTERACTIVE GRID TILES (pl.State Handling)
    # ============================================================
    interactive_grid = pl.grid(
        pl.button("Select 1", on_click=select_card_1, style=pl.style(padding="1rem", cursor="pointer")),
        pl.button("Select 2", on_click=select_card_2, style=pl.style(padding="1rem", cursor="pointer")),
        pl.button("Select 3", on_click=select_card_3, style=pl.style(padding="1rem", cursor="pointer")),
        pl.button("Select 4", on_click=select_card_4, style=pl.style(padding="1rem", cursor="pointer")),
        style=pl.style(
            grid_template_columns="repeat(2, 1fr)",
            gap="1rem",
            padding="1rem",
            background_color="#eff6ff",
            border="1px dashed #2563eb",
            border_radius="0.5rem",
            margin_bottom="1.5rem",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage Grid — Live Manual",
            style=pl.style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        pl.text(
            "Grid layout component ke multi-column, template ratio, aur responsive grid features test karein:",
            style=pl.style(color="#64748b", margin_bottom="1.5rem"),
        ),

        pl.text("1. Equal 3-pl.column Grid (`repeat(3, 1fr)`)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        fixed_grid,

        pl.text("2. Asymmetric Grid Layout (`1fr 3fr`)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        asymmetric_grid,

        pl.text("3. Responsive Auto-Fit Grid (`minmax(140px, 1fr)`)", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        responsive_grid,

        pl.text("4. Interactive Grid Tile Selection", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        pl.row(
            pl.text("Active Selection: ", style=pl.style(font_weight="600")),
            pl.heading(selected_card, style=pl.style(color="#2563eb", font_size="1rem")),
            style=pl.style(gap="0.5rem", margin_bottom="0.5rem", align_items="center"),
        ),
        interactive_grid,

        style=pl.style(
            width="100%",
            max_width="750px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )
