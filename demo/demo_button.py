import pylage as pl
import sys
from pathlib import Path

# Ensure local pylage import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps

def get_app():
    # 1. Exact Working Pattern: Reactive pl.State
    count = pl.state(0)

    # 2. Exact Working Pattern: Callback function
    def handle_click():
        count.set(count.value + 1)
        return count.value

    # 3. Direct pl.State object bound to pl.heading
    status = pl.heading(count)

    # 4. Buttons initialization with exact test-case syntax (on_click=handle_click)
    basic = pl.button("Basic pl.button", on_click=handle_click)

    primary = pl.button(
        "Primary pl.button",
        on_click=handle_click,
        style=pl.style(
            background_color="#2563eb",
            color="#ffffff",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    large = pl.button(
        "Large pl.button",
        on_click=handle_click,
        style=pl.style(
            background_color="#7c3aed",
            color="#ffffff",
            padding="1rem 2rem",
            font_size="1.1rem",
            font_weight="700",
            border_radius="0.75rem",
            cursor="pointer",
        ),
    )

    outline = pl.button(
        "Outline pl.button",
        on_click=handle_click,
        style=pl.style(
            background_color="#ffffff",
            color="#2563eb",
            border="1px solid #2563eb",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    danger = pl.button(
        "Delete",
        on_click=handle_click,
        style=pl.style(
            background_color="#dc2626",
            color="#ffffff",
            padding="0.75rem 1.25rem",
            border_radius="0.5rem",
            font_weight="700",
            cursor="pointer",
        ),
    )

    custom = pl.button(
        "Custom pl.button",
        on_click=handle_click,
        style=pl.style(
            background_color="#fef3c7",
            color="#92400e",
            border="2px solid #f59e0b",
            border_radius="999px",
            padding="0.75rem 1.5rem",
            font_weight="700",
            box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1)",
            cursor="pointer",
        ),
    )

    return pl.column(
        pl.text(
            "PyLage pl.button — Live Manual",
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                color="#0f172a",
                margin_bottom="0.5rem",
            ),
        ),
        pl.text(
            "pl.button click count test karne ke liye niche buttons par click karo:",
            style=pl.style(color="#64748b", margin_bottom="1.5rem"),
        ),

        # pl.State output component
        status,

        pl.text("Basic", style=pl.style(font_weight="700", margin_bottom="0.5rem")),
        basic,

        pl.text("Primary", style=pl.style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        primary,

        pl.text("Large", style=pl.style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        large,

        pl.text("Outline", style=pl.style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        outline,

        pl.text("Danger", style=pl.style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        danger,

        pl.text("Custom", style=pl.style(font_weight="700", margin_top="1.5rem", margin_bottom="0.5rem")),
        custom,

        style=pl.style(
            width="100%",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    )
