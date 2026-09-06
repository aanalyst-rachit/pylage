"""
Voltra — a small reactive SaaS demo built with PyLage.

Only the public API is used throughout (import pylage as pl).
No ENGINE internals, no direct registry/renderer access — everything
here is something you could point a new pylage user at as a reference.
"""

import pylage as pl

# ---------------------------------------------------------------------------
# Global Theme Configuration
# ---------------------------------------------------------------------------
pl.set_theme("dark")

# ---------------------------------------------------------------------------
# Reactive State Definitions
# ---------------------------------------------------------------------------
signups = pl.State(1284)
revenue = pl.State("$18,420")
teams = pl.State(342)

toast_visible = pl.State(False)

plan_name = pl.State("Pro")
plan_price = pl.State("$29/mo")
starter_active = pl.State(False)
pro_active = pl.State(True)
enterprise_active = pl.State(False)


# ---------------------------------------------------------------------------
# Event Handlers & Business Logic
# ---------------------------------------------------------------------------
def simulate_signup(payload=None):
    signups.set(signups.value + 1)
    teams.set(teams.value + (1 if signups.value % 4 == 0 else 0))
    toast_visible.set(True)


def dismiss_toast(payload=None):
    toast_visible.set(False)


def choose_plan(name, price):
    def handler(payload=None):
        plan_name.set(name)
        plan_price.set(price)
        starter_active.set(name == "Starter")
        pro_active.set(name == "Pro")
        enterprise_active.set(name == "Enterprise")

    return handler


def subscribe_clicked(payload=None):
    toast_visible.set(True)


# ---------------------------------------------------------------------------
# Isolated Design System / Centralized Style Class
# ---------------------------------------------------------------------------
class STYLES:
    # Main Page Wrapper
    PAGE = pl.style(
        display="flex",
        flex_direction="column",
        width="100%",
        max_width="1080px",
        margin="0 auto",
        padding="1.5rem 1rem 4rem",
        gap="3rem",
        background_color="#090d16",
        color="#f8fafc",
        font_family="'Inter', system-ui, -apple-system, sans-serif",
        box_sizing="border-box",
    )

    # Generic Reusable Cards
    CARD_GLASS = pl.style(
        background="rgba(30, 41, 59, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="0.75rem",
        padding="1.25rem",
        box_sizing="border-box",
        width="100%",
    )

    # Dashboard Sections
    SECTION = pl.style(
        background="rgba(15, 23, 42, 0.4)",
        border="1px solid rgba(255, 255, 255, 0.05)",
        border_radius="1rem",
        padding="1.75rem",
        width="100%",
        box_sizing="border-box",
    )

    # Top Navbar Styling Fix
    NAVBAR_CONTAINER = pl.style(
        display="flex",
        align_items="center",
        justify_content="space-between",
        width="100%",
        padding="0.75rem 1.25rem",
        border_radius="0.75rem",
        background="rgba(15, 23, 42, 0.8)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        box_sizing="border-box",
    )

    NAV_LOGO = pl.style(
        font_size="1.25rem",
        font_weight="800",
        letter_spacing="-0.02em",
        color="#38bdf8",
        # NEED TO BE ADDED IN LIBRARY (Style Class):
        # text_shadow="0 0 12px rgba(56, 189, 248, 0.4)",
    )

    NAV_ROW = pl.style(gap="1.25rem", align_items="center")

    NAV_BUTTON = pl.style(
        border_radius="0.5rem",
        font_weight="600",
        padding="0.4rem 0.85rem",
    )

    # Hero Centering & Layout Fix
    HERO_WRAPPER = pl.style(
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        text_align="center",
        width="100%",
        padding="3rem 1rem 1.5rem",
        box_sizing="border-box",
    )

    HERO_ACTIONS_ROW = pl.style(
        display="flex",
        justify_content="center",
        align_items="center",
        gap="1rem",
        margin_top="1.5rem",
        width="100%",
    )

    HERO_PRIMARY_BTN = pl.style(
        background="#0284c7",
        color="#ffffff",
        border="none",
        border_radius="0.5rem",
        font_weight="600",
        padding="0.6rem 1.25rem",
    )

    HERO_SECONDARY_BTN = pl.style(
        border="1px solid rgba(255, 255, 255, 0.2)",
        border_radius="0.5rem",
        font_weight="600",
        padding="0.6rem 1.25rem",
    )

    # Metrics Section
    STAT_GROUP = pl.style(gap="1.25rem", width="100%")

    LIVE_BADGE = pl.style(
        padding="0.2rem 0.6rem",
        border_radius="9999px",
        font_weight="700",
    )

    # Pricing & Plan Selection
    PLAN_TABS = pl.style(
        gap="0.5rem",
        background="rgba(30, 41, 59, 0.6)",
        padding="0.3rem",
        border_radius="0.5rem",
        border="1px solid rgba(255, 255, 255, 0.05)",
    )

    SUBSCRIBE_BTN = pl.style(
        margin_top="1rem",
        width="100%",
        background="#0284c7",
        color="#ffffff",
        font_weight="700",
        border_radius="0.5rem",
        padding="0.6rem",
    )

    # Features Grid Row
    FEATURES_ROW = pl.style(gap="1.25rem", width="100%")

    # Footer
    FOOTER = pl.style(
        padding="1.5rem 0 1rem",
        border_top="1px solid rgba(255, 255, 255, 0.05)",
        text_align="center",
        width="100%",
    )

    FOOTER_TEXT = pl.style(letter_spacing="0.05em", color="#64748b")

    # Toast Overlay
    TOAST_TEXT = pl.style(font_weight="600")

    TOAST_CONTAINER = pl.style(
        position="fixed",
        bottom="1.5rem",
        right="1.5rem",
        max_width="320px",
        padding="0.85rem 1rem",
        background="rgba(15, 23, 42, 0.95)",
        border="1px solid #22c55e",
        border_radius="0.5rem",
        z_index=1000,
        # NEED TO BE ADDED IN LIBRARY (Style Class):
        # backdrop_filter="blur(8px)",
    )


# Backward-compatible style alias
PAGE_STYLE = STYLES.PAGE

# ---------------------------------------------------------------------------
# Component Layout Assembly
# ---------------------------------------------------------------------------

# Top Navigation Bar
top_bar = pl.navbar(
    pl.text("⚡ Voltra", label=True, style=STYLES.NAV_LOGO),
    pl.row(
        pl.navigation_item("Home", active=True),
        pl.navigation_item("Pricing", active=False),
        pl.navigation_item("Docs", active=False),
        style=STYLES.NAV_ROW,
    ),  # type: ignore
    pl.button(
        "Simulate signup",
        on_click=simulate_signup,
        variant="secondary",
        size="sm",
        style=STYLES.NAV_BUTTON,
    ),
    style=STYLES.NAVBAR_CONTAINER,
)  # pyright: ignore[reportCallIssue]

# Hero Section
hero = pl.column(
    pl.text(
        "Ship your SaaS 10x faster",
        style=pl.style(
            font_size="2.25rem",
            font_weight="800",
            text_align="center",
            line_height="1.2",
        ),
    ),
    pl.text(
        "Voltra gives your team a reactive, batteries-included dashboard "
        "so you can focus on the product instead of the plumbing.",
        style=pl.style(
            font_size="1rem",
            color="#94a3b8",
            text_align="center",
            margin_top="0.75rem",
            max_width="650px",
        ),
    ),
    pl.row(
        pl.button(
            "Start free trial",
            on_click=simulate_signup,
            size="lg",
            style=STYLES.HERO_PRIMARY_BTN,
        ),
        pl.button(
            "View plans",
            variant="outline",
            size="lg",
            style=STYLES.HERO_SECONDARY_BTN,
        ),
        style=STYLES.HERO_ACTIONS_ROW,
    ),
    style=STYLES.HERO_WRAPPER,
)

# Metrics Dashboard Section
stats_section = pl.dashboard_section(
    pl.stat_group(
        pl.metric("Signups", signups, delta="+12% this week"),
        pl.metric("Monthly revenue", revenue, delta="+8% this week"),
        pl.metric("Active teams", teams, delta="+4% this week"),
        style=STYLES.STAT_GROUP,
    ),
    title="Live metrics",
    description="Updates instantly over the wire as your customers act.",
    action=pl.badge(
        "Live",
        variant="success",
        style=STYLES.LIVE_BADGE,
    ),
    style=STYLES.SECTION,
)

# Pricing Options & Cards
plan_options = pl.row(
    pl.navigation_item("Starter", active=starter_active, on_click=choose_plan("Starter", "$9/mo")),
    pl.navigation_item("Pro", active=pro_active, on_click=choose_plan("Pro", "$29/mo")),
    pl.navigation_item("Enterprise", active=enterprise_active, on_click=choose_plan("Enterprise", "Custom")),
    style=STYLES.PLAN_TABS,
)  # type: ignore

plan_summary = pl.card(
    pl.button(
        "Subscribe",
        on_click=subscribe_clicked,
        style=STYLES.SUBSCRIBE_BTN,
    ),
    heading=plan_name,
    body=plan_price,
    variant="elevated",
    style=STYLES.CARD_GLASS,
)

pricing_section = pl.dashboard_section(
    plan_options,
    plan_summary,
    title="Choose your plan",
    description="Switch anytime — no credit card required for the trial.",
    style=STYLES.SECTION,
)

# Features Grid Section
features_section = pl.dashboard_section(
    pl.row(
        pl.card(
            heading="Realtime by default",
            body="Every State change reaches the browser over one shared WebSocket connection.",
            style=STYLES.CARD_GLASS,
        ),
        pl.card(
            heading="Composable UI kit",
            body="Buttons, cards, forms and layouts that already know your theme tokens.",
            style=STYLES.CARD_GLASS,
        ),
        pl.card(
            heading="No build step",
            body="Write Python, get a reactive web app — no bundler, no JSX.",
            style=STYLES.CARD_GLASS,
        ),
        style=STYLES.FEATURES_ROW,
    ),  # type: ignore
    title="Why teams pick Voltra",
    style=STYLES.SECTION,
)

# Footer Component
footer = pl.Footer(
    pl.text(
        "© 2026 Voltra Inc. — built with PyLage.",
        muted=True,
        caption=True,
        style=STYLES.FOOTER_TEXT,
    ),
    style=STYLES.FOOTER,
)

# Live Toast Overlay
live_toast = pl.toast(
    pl.text("🎉 New signup recorded!", style=STYLES.TOAST_TEXT),
    pl.button("Dismiss", on_click=dismiss_toast, size="sm", variant="ghost"),
    variant="success",
    visible=toast_visible,
    style=STYLES.TOAST_CONTAINER,
)

# Main Application Root Container
app = pl.Container(
    top_bar,
    hero,
    stats_section,
    pricing_section,
    features_section,
    footer,
    live_toast,
    style=STYLES.PAGE,
)

# ---------------------------------------------------------------------------
# Execution Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    pl.run(app, title="Voltra", output="voltra_demo.html", serve=True, host="0.0.0.0", port=3000)
    print("Rendered voltra_demo.html")