import pylage as pl
"""Manual demonstration for the PyLage UI Kit trend component."""

import pylage as ps

# ==========================================
# 1. STYLES DEFINITION (INCREASED TEXT SIZES)
# ==========================================
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, sans-serif"

CONTAINER_STYLE = pl.style(
    padding="2.5rem",
    display="flex",
    flex_direction="column",
    gap="1.75rem",
    max_width="950px",
    margin="0 auto",
    font_family=FONT_FAMILY,
)

# Bada pl.heading Size (2rem -> 2.5rem)
TITLE_STYLE = pl.style(
    font_size="2.5rem",
    font_weight="800",
    color="#0f172a",
    letter_spacing="-0.02em",
)

# Bada Subtitle Size (1rem -> 1.15rem)
SUBTITLE_STYLE = pl.style(
    color="#64748b",
    font_size="1.15rem",
    margin_bottom="1.25rem",
    line_height="1.5",
)

# Bada Section Title Size (1.125rem -> 1.35rem)
SECTION_TITLE_STYLE = pl.style(
    font_size="1.35rem",
    font_weight="700",
    color="#0f172a",
    margin_bottom="1rem",
)

SECTION_CARD_STYLE = pl.style(
    background="#ffffff",
    border="1px solid #e2e8f0",
    border_radius="14px",
    padding="1.75rem",
    box_shadow="0 1px 3px rgba(0, 0, 0, 0.05)",
    width="100%",
)

# Elevated Drop-Shadow + Increased Font Size for Trend Badges
TREND_ELEVATED_STYLE = pl.style(
    box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.05)",
    border_radius="6px",
    display="inline-flex",
    max_width="fit-content",
    font_size="0.95rem",  # Badges ka text size bhi thoda bda kiya
    padding="0.25rem 0.5rem",
)

COMPACT_TREND_CONTAINER = pl.style(
    display="flex",
    flex_direction="column",
    align_items="flex-start",
    gap="0.85rem",
)

ROW_LAYOUT_STYLE = pl.style(
    display="flex",
    align_items="center",
    gap="1.25rem",
    flex_wrap="wrap",
)

FEATURED_CARD_STYLE = pl.style(
    background="#ffffff",
    border="1.5px solid #3b82f6",
    border_radius="12px",
    padding="1.5rem",
    box_shadow="0 4px 12px -2px rgba(59, 130, 246, 0.12)",
    display="flex",
    flex_direction="column",
    gap="1rem",
    max_width="450px",
)


# ==========================================
# HELPER WRAPPER
# ==========================================
def section_card(title: str, content) -> pl.column:
    return pl.column(
        pl.heading(title, level=2, style=SECTION_TITLE_STYLE),
        content,
        style=SECTION_CARD_STYLE,
    )


# ==========================================
# MAIN APP
# ==========================================
def get_app() -> pl.column:
    return pl.column(
        # Main Header Section
        pl.heading("PyLage UI Kit — Trend", level=1, style=TITLE_STYLE),
        pl.text(
            "Semantic directional indicators for dashboards, metrics, and data-driven interfaces.",
            style=SUBTITLE_STYLE,
        ),

        # Section 1: Automatic Direction Detection
        section_card(
            "Automatic Direction Detection",
            pl.row(
                ps.trend("+12%", style=TREND_ELEVATED_STYLE),
                ps.trend("-8.5%", style=TREND_ELEVATED_STYLE),
                ps.trend("0%", style=TREND_ELEVATED_STYLE),
                style=ROW_LAYOUT_STYLE,
            ),
        ),

        # Section 2: Explicit Direction
        section_card(
            "Explicit Direction",
            pl.column(
                ps.trend("Revenue increased", direction="up", style=TREND_ELEVATED_STYLE),
                ps.trend("Traffic declined", direction="down", style=TREND_ELEVATED_STYLE),
                ps.trend("Performance stable", direction="neutral", style=TREND_ELEVATED_STYLE),
                style=COMPACT_TREND_CONTAINER,
            ),
        ),

        # Section 3: Indicator Control
        section_card(
            "Indicator Control",
            pl.row(
                ps.trend("+24%", style=TREND_ELEVATED_STYLE),
                ps.trend("+24%", show_indicator=False, style=TREND_ELEVATED_STYLE),
                style=ROW_LAYOUT_STYLE,
            ),
        ),

        # Section 4: Metric + Trend Dashboard Pattern
        section_card(
            "Metric + Trend Dashboard Pattern",
            pl.column(
                ps.metric(
                    label="Monthly Revenue",
                    value="₹42,000",
                    description="Current month performance",
                ),
                ps.trend(
                    "+12% compared with last month",
                    direction="up",
                    style=TREND_ELEVATED_STYLE,
                ),
                style=FEATURED_CARD_STYLE,
            ),
        ),

        style=CONTAINER_STYLE,
    )