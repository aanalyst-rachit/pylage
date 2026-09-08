import pylage as pl



# ============================================================
# 1. Global page style (Light Theme)
# ============================================================

page_style = pl.style(
    width="100%",
    min_height="100vh",
    background_color="#f8fafc",  # Light slate background
    color="#0f172a",             # Dark slate text
    box_sizing="border-box",
)


# ============================================================
# 2. Header
# ============================================================

header = pl.row(
    pl.text(
        "PyLage Dashboard",
        style=pl.style(
            font_size="1.35rem",
            font_weight="700",
            color="#0f172a",
        ),
    ),
    pl.card(
        "Admin Console",
        style=pl.style(
            font_size="0.9rem",
            color="#64748b",
        ),
    ),
    style=pl.style(
        width="100%",
        display="flex",
        flex_direction="row",
        justify_content="space-between",
        align_items="center",
        padding="1.25rem 2rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 3. Sidebar
# ============================================================

sidebar = pl.column(
    pl.text(
        "NAVIGATION",
        style=pl.style(
            font_size="0.75rem",
            font_weight="700",
            color="#94a3b8",
            margin_bottom="1rem",
        ),
    ),

    pl.text(
        "▣  Dashboard",
        style=pl.style(
            padding="0.75rem",
            background_color="#eff6ff",
            color="#1d4ed8",
            border="1px solid #bfdbfe",
            border_radius="0.5rem",
            font_weight="600",
            margin_bottom="0.5rem",
        ),
    ),

    pl.text(
        "▤  Analytics",
        style=pl.style(
            padding="0.75rem",
            color="#475569",
            margin_bottom="0.5rem",
        ),
    ),

    pl.text(
        "◉  Customers",
        style=pl.style(
            padding="0.75rem",
            color="#475569",
            margin_bottom="0.5rem",
        ),
    ),

    pl.text(
        "⚙  Settings",
        style=pl.style(
            padding="0.75rem",
            color="#475569",
        ),
    ),

    style=pl.style(
        width="260px",
        min_width="260px",
        padding="1.5rem",
        background_color="#ffffff",
        color="#334155",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 4. Hero
# ============================================================

def on_get_started():
    print("GET STARTED CLICKED")


def on_view_documentation():
    print("VIEW DOCUMENTATION CLICKED")


hero = pl.hero(
    title="Build dashboards without fighting layout",

    description=(
        "A responsive dashboard composed entirely from "
        "reusable pylage_layout primitives and patterns."
    ),

    actions=[
        pl.text(
            "Get Started",
            style=pl.style(
                padding="0.6rem 1.2rem",
                background_color="#2563eb",
                color="#ffffff",
                border_radius="0.375rem",
                font_weight="600",
                margin_right="0.75rem",
            ),
        ).on("click", on_get_started),

        pl.text(
            "View Documentation",
            style=pl.style(
                padding="0.6rem 1.2rem",
                background_color="#ffffff",
                color="#1e293b",
                border="1px solid #cbd5e1",
                border_radius="0.375rem",
                font_weight="600",
            ),
        ).on("click", on_view_documentation),
    ],

    style=pl.style(
        width="100%",
        padding="2rem",
        background_color="#eff6ff",
        color="#1e3a8a",
        border="1px solid #bfdbfe",
        border_radius="0.75rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        box_sizing="border-box",
    ),
)


# ============================================================
# 5. Statistics
# ============================================================

stats = pl.stats_section(
    title="Overview",

    description="Current application metrics",

    stats=[
        {
            "value": "12.8K",
            "label": "Total Users",
            "description": "+18.4% this month",
        },
        {
            "value": "8.42K",
            "label": "Active Users",
            "description": "+12.7% this month",
        },
        {
            "value": "$48.2K",
            "label": "Revenue",
            "description": "+24.1% this month",
        },
        {
            "value": "94.8%",
            "label": "Conversion",
            "description": "+4.2% this month",
        },
    ],

    style=pl.style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 6. Feature section
# ============================================================

features = pl.feature_section(
    {
        "title": "Design Tokens",
        "description": (
            "Consistent spacing, colors, typography and radius."
        ),
    },

    {
        "title": "Responsive Layout",
        "description": (
            "Mobile-first layouts using ResponsiveStyle."
        ),
    },

    {
        "title": "Reusable Patterns",
        "description": (
            "Build complex pages from small compositions."
        ),
    },

    {
        "title": "Theme Ready",
        "description": (
            "Design systems can be connected to reusable themes."
        ),
    },

    title="Why pylage_layout?",

    description=(
        "Everything is composed from reusable building blocks."
    ),

    style=pl.style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 7. Analytics
# ============================================================

analytics = pl.content_section(
    title="Analytics",

    content=(
        "Your application is growing steadily. "
        "Revenue and active users are both trending upward."
    ),

    actions=[
        pl.text(
            "Revenue ↑ 24.1%",
            style=pl.style(
                padding="0.75rem 1rem",
                background_color="#dcfce7",
                color="#166534",
                border="1px solid #bbf7d0",
                border_radius="0.5rem",
                margin_right="0.75rem",
            ),
        ),

        pl.text(
            "Users ↑ 18.4%",
            style=pl.style(
                padding="0.75rem 1rem",
                background_color="#dbeafe",
                color="#1e40af",
                border="1px solid #bfdbfe",
                border_radius="0.5rem",
            ),
        ),
    ],

    style=pl.style(
        width="100%",
        padding="2rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 8. Pricing
# ============================================================

pricing = pl.pricing_section(
    title="Plans",

    description="Choose the plan that fits your team.",

    plans=[
        {
            "name": "Starter",
            "price": "$9",
            "description": "For individuals.",
            "features": [
                "1 project",
                "Basic analytics",
                "Community support",
            ],
            "action": "Start Starter",
        },

        {
            "name": "Professional",
            "price": "$29",
            "description": "For growing teams.",
            "features": [
                "10 projects",
                "Advanced analytics",
                "Priority support",
            ],
            "action": "Choose Pro",
            "featured": True,
        },

        {
            "name": "Enterprise",
            "price": "$99",
            "description": "For larger organizations.",
            "features": [
                "Unlimited projects",
                "Advanced security",
                "Dedicated support",
            ],
            "action": "Contact Sales",
        },
    ],

    style=pl.style(
        width="100%",
        padding="1.5rem",
        background_color="#ffffff",
        color="#0f172a",
        border="1px solid #e2e8f0",
        border_radius="0.75rem",
        box_sizing="border-box",
    ),
)


# ============================================================
# 9. CTA
# ============================================================

cta = pl.cta(
    title="Ready to ship faster?",

    description=(
        "Compose responsive pages with PyLage Layout "
        "instead of rebuilding layouts from scratch."
    ),

    actions=[
        pl.text(
            "Install Now",
            style=pl.style(
                padding="0.75rem 1.5rem",
                background_color="#4338ca",
                color="#ffffff",
                border_radius="0.5rem",
                font_weight="600",
                display="inline-block",
            ),
        ),
    ],

    style=pl.style(
        width="100%",
        padding="2rem",
        background_color="#eef2ff",
        color="#312e81",
        border="1px solid #c7d2fe",
        border_radius="0.75rem",
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.05)",
        box_sizing="border-box",
    ),
)


# ============================================================
# 10. Footer
# ============================================================

footer = pl.footer(
    pl.text(
        "PyLage Layout • Responsive UI composition for Python",
        style=pl.style(
            color="#64748b",
            font_size="0.85rem",
        ),
    ),

    style=pl.style(
        width="100%",
        padding="1.5rem 2rem",
        background_color="#ffffff",
        color="#64748b",
        border="1px solid #e2e8f0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 11. Dashboard content
# ============================================================

dashboard_content = pl.column(
    hero,
    stats,
    features,
    analytics,
    pricing,
    cta,
    footer,

    style=pl.style(
        width="100%",
        min_width="0",
        display="flex",
        flex_direction="column",
        gap="1.5rem",
        padding="1.5rem",
        background_color="#f8fafc",
        color="#0f172a",
        box_sizing="border-box",
    ),
)


# ============================================================
# 12. Main two-column layout
# ============================================================

columns = pl.twocolumn(
    sidebar,

    pl.container(
        dashboard_content,

        style=pl.style(
            width="100%",
            min_width="0",
            max_width="100%",
            background_color="#f8fafc",
            color="#0f172a",
            box_sizing="border-box",
        ),
    ),

    style=pl.style(
        width="100%",
        display="flex",
        flex_direction="row",
        gap="0",
        box_sizing="border-box",
    ),
)


# ============================================================
# 13. Application shell
# ============================================================

app = pl.appshell(
    header=header,
    content=columns,
    style=page_style,
)


# ============================================================
# 14. Run
# ============================================================

def get_app():
    return app
