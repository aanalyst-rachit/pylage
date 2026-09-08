import pylage as pl
"""Manual demo for PyLage Design Tokens & Theme Engine (Tokens, Light, Dark, Factory)."""

from pylage.ENGINE import Theme
from pylage.UI.tokens import COLORS, FONTS, RADIUS, SPACING, validate_tokens
from pylage.UI.themes.light import LIGHT_THEME
from pylage.UI.themes.dark import DARK_THEME


def get_app() -> pl.column:
    is_dark = pl.state(False)

    title = pl.heading("🎨 Design Tokens & Theme System Manual", level=1)
    desc = pl.text(
        "Demonstrates design tokens, color scales, typography mappings, and dynamic theme switching.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # 1. Token validation card
    is_valid = validate_tokens()
    token_status = pl.card(
        pl.heading("1. Design Tokens Status", level=3),
        pl.row(
            pl.text("Token Engine Status: "),
            pl.badge("VALIDATED ✅" if is_valid else "INVALID ❌", variant="success" if is_valid else "danger"),
            style=pl.style(align_items="center", gap="0.75rem", margin_top="0.5rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 2. Color Palette Swatches
    color_swatches = []
    for key, hex_val in list(COLORS.items())[:8]:
        color_swatches.append(
            pl.column(
                pl.row(
                    style=pl.style(
                        width="36px",
                        height="36px",
                        background=hex_val,
                        border_radius="0.375rem",
                        border="1px solid #e2e8f0",
                    )
                ),
                pl.text(key, style=pl.style(font_size="0.75rem", font_weight="bold", margin_top="0.25rem")),
                pl.text(hex_val, style=pl.style(font_size="0.675rem", color="#64748b")),
                style=pl.style(align_items="center", min_width="80px"),
            )
        )

    palette_card = pl.card(
        pl.heading("2. Token Color Palette Swatches", level=3),
        pl.row(*color_swatches, style=pl.style(gap="1rem", flex_wrap="wrap", margin_top="0.75rem")),
        style=pl.style(padding="1.25rem", margin_bottom="1.5rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 3. Theme Toggle pl.card
    theme_card = pl.card(
        pl.heading("3. Theme Switcher", level=3),
        pl.text("Toggle between light and dark design tokens:"),
        pl.row(
            pl.button("Switch Theme Mode", on_click=lambda: is_dark.set(not is_dark.value)),
            pl.badge("Mode: Dark" if is_dark.value else "Mode: Light", variant="primary"),
            style=pl.style(align_items="center", gap="1rem", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        token_status,
        palette_card,
        theme_card,
        style=pl.style(padding="2rem", max_width="1000px", margin="0 auto"),
    )
