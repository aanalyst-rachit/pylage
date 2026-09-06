import pylage as pl


def metric_card(label, value, delta=None, description=None, featured=False):
    is_positive = delta and delta.startswith("+")
    delta_bg = "#dcfce7" if is_positive else "#fee2e2"
    delta_color = "#15803d" if is_positive else "#b91c1c"

    card_style = pl.style(
        background="#ffffff" if not featured else "linear-gradient(180deg, #ffffff 0%, #f0f9ff 100%)",
        border="1px solid #e2e8f0" if not featured else "1.5px solid #3b82f6",
        border_radius="12px",
        padding="1.25rem 1.5rem",
        box_shadow="0 4px 6px -1px rgba(0,0,0,0.05)" if not featured else "0 8px 16px -2px rgba(59, 130, 246, 0.15)",
        flex="1",
        min_width="260px",
        font_family="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
    )

    return pl.column(
        pl.text(
            label,
            style=pl.style(
                color="#64748b",
                font_size="0.875rem",
                font_weight="500",
                margin_bottom="0.5rem",
            ),
        ),
        pl.text(
            value,
            style=pl.style(
                color="#0f172a",
                font_size="2rem",
                font_weight="700",
                line_height="1.2",
                margin_bottom="0.75rem",
            ),
        ),
        # Inner Footer pl.row with CSS gap
        pl.row(
            pl.text(
                delta,
                style=pl.style(
                    background=delta_bg,
                    color=delta_color,
                    font_size="0.75rem",
                    font_weight="600",
                    padding="0.2rem 0.5rem",
                    border_radius="6px",
                ),
            ) if delta else None,
            pl.text(
                description,
                style=pl.style(
                    color="#94a3b8",
                    font_size="0.75rem",
                ),
            ) if description else None,
            style=pl.style(display="flex", align_items="center", gap="0.5rem"),
        ),
        style=card_style,
    )


def get_app():
    return pl.column(
        pl.text(
            "Metric",
            style=pl.style(
                font_size="2rem",
                font_weight="700",
                color="#0f172a",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.text(
            "Custom styled SaaS KPI dashboard cards built using PyLage primitives.",
            style=pl.style(
                color="#64748b",
                margin_bottom="1.5rem",
                font_family="Inter, sans-serif",
            ),
        ),

        # Main Metric pl.row — Explicit CSS gap inside pl.style()
        pl.row(
            metric_card(
                label="Revenue",
                value="₹42,000",
                delta="+12%",
                description="vs last month",
            ),
            metric_card(
                label="Users",
                value="12,450",
                delta="+8.4%",
                description="active users",
            ),
            metric_card(
                label="Latency",
                value="4.2ms",
                delta="-18.5%",
                description="vs previous period",
            ),
            style=pl.style(
                display="flex",
                flex_wrap="wrap",
                width="100%",
                gap="1.5rem"  # Direct CSS Gap Fix
            ),
        ),

        pl.text(
            "Featured Variant:",
            style=pl.style(
                color="#0f172a",
                font_weight="600",
                margin_top="2rem",
                font_family="Inter, sans-serif",
            ),
        ),
        pl.row(
            metric_card(
                label="Orders",
                value="1,284",
                delta="+5.2%",
                description="updated just now",
                featured=True,
            )
        ),
        style=pl.style(
            padding="2rem",
            max_width="1100px",
            margin="0 auto",
            font_family="Inter, sans-serif",
            display="flex",
            flex_direction="column",
            gap="1.5rem"
        ),
    )