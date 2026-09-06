"""
Voltra — a small reactive SaaS demo built with PyLage.

Only the public API is used throughout (import pylage as pl).
No ENGINE internals, no direct registry/renderer access — everything
here is something you could point a new pylage user at as a reference.
"""

import pylage as pl

pl.set_theme("dark")

# ---------------------------------------------------------------------------
# Reactive state
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
# Layout pieces
# ---------------------------------------------------------------------------

# Page-level containers must NOT inherit the framework's default
# "row on desktop, column on mobile" responsive style, so every
# vertical stack below gets an explicit flex_direction="column".
PAGE_STYLE = pl.style(
    display="flex",
    flex_direction="column",
    width="100%",
    max_width="1080px",
    margin="0 auto",
    padding="0 1.5rem 4rem",
    gap="3rem",
)

top_bar = pl.navbar(
    pl.text("⚡ Voltra", label=True, style=pl.style(font_size="1.25rem", font_weight="700")),
    pl.row(
        pl.navigation_item("Home", active=True),
        pl.navigation_item("Pricing", active=False),
        pl.navigation_item("Docs", active=False),
    ),
    pl.button("Simulate signup", on_click=simulate_signup, variant="secondary", size="sm"),
)

hero = pl.Hero(
    "Ship your SaaS 10x faster",
    "Voltra gives your team a reactive, batteries-included dashboard "
    "so you can focus on the product instead of the plumbing.",
    actions=[
        pl.button("Start free trial", on_click=simulate_signup, size="lg"),
        pl.button("View plans", variant="outline", size="lg"),
    ],
)

stats_section = pl.dashboard_section(
    pl.stat_group(
        pl.metric("Signups", signups, delta="+12% this week"),
        pl.metric("Monthly revenue", revenue, delta="+8% this week"),
        pl.metric("Active teams", teams, delta="+4% this week"),
    ),
    title="Live metrics",
    description="Updates instantly over the wire as your customers act.",
    action=pl.badge("Live", variant="success"),
)

plan_options = pl.row(
    pl.navigation_item("Starter", active=starter_active, on_click=choose_plan("Starter", "$9/mo")),
    pl.navigation_item("Pro", active=pro_active, on_click=choose_plan("Pro", "$29/mo")),
    pl.navigation_item("Enterprise", active=enterprise_active, on_click=choose_plan("Enterprise", "Custom")),
)

plan_summary = pl.card(
    pl.button("Subscribe", on_click=subscribe_clicked, style=pl.style(margin_top="0.5rem")),
    heading=plan_name,
    body=plan_price,
    variant="elevated",
)

pricing_section = pl.dashboard_section(
    plan_options,
    plan_summary,
    title="Choose your plan",
    description="Switch anytime — no credit card required for the trial.",
)

features_section = pl.dashboard_section(
    pl.row(
        pl.card(heading="Realtime by default", body="Every State change reaches the browser over one shared WebSocket connection."),
        pl.card(heading="Composable UI kit", body="Buttons, cards, forms and layouts that already know your theme tokens."),
        pl.card(heading="No build step", body="Write Python, get a reactive web app — no bundler, no JSX."),
    ),
    title="Why teams pick Voltra",
)

footer = pl.Footer(
    pl.text("© 2026 Voltra Inc. — built with PyLage.", muted=True, caption=True),
)

live_toast = pl.toast(
    pl.text("🎉 New signup recorded!"),
    pl.button("Dismiss", on_click=dismiss_toast, size="sm", variant="ghost"),
    variant="success",
    visible=toast_visible,
    style=pl.style(
        position="fixed",
        bottom="1.5rem",
        right="1.5rem",
        max_width="320px",
        box_shadow="0 10px 25px rgba(0,0,0,0.35)",
        z_index=1000,
    ),
)

app = pl.Container(
    top_bar,
    hero,
    stats_section,
    pricing_section,
    features_section,
    footer,
    live_toast,
    style=PAGE_STYLE,
)


if __name__ == "__main__":
    # File-only render (no server). For a live reactive server run:
    #   pl.run(app, title="Voltra", serve=True)
    pl.run(app, title="Voltra", output="voltra_demo.html", serve=True, host="0.0.0.0", port=3000)
    print("Rendered voltra_demo.html")