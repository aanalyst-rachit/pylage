import pylage as pl
import pylage as ps


def get_app():
    # 1. Subtle Glow / Shadow Divider
    shadow_divider = pl.style(
        border="none",
        height="1px",
        background_color="#e2e8f0",
        box_shadow="0 2px 4px 0 rgba(0, 0, 0, 0.15)",
        margin="1.5rem 0"
    )

    # 2. Modern Faded Gradient Divider (Edges Par Fade Out Control)
    gradient_divider = pl.style(
        border="none",
        height="2px",
        background="linear-gradient(to right, transparent, #94a3b8, transparent)",
        margin="1.5rem 0"
    )

    # 3. Soft Inset / Carved Shadow Divider
    inset_divider = pl.style(
        border="none",
        height="1px",
        background_color="#cbd5e1",
        box_shadow="0 1px 2px 0 rgba(0, 0, 0, 0.08)",
        margin="1.5rem 0"
    )

    return pl.column(
        ps.heading("Divider"),
        ps.text("Semantic horizontal separators with sensible UI Kit defaults."),

        ps.text("Above divider"),
        # Modern Gradient Divider
        ps.divider(style=gradient_divider),

        ps.text("Below divider"),
        # Soft Shadow Divider
        ps.divider(style=shadow_divider),

        pl.row(
            ps.text("Custom content"),
            gap="0.75rem",
        ),
        # Inset Shadow Divider
        ps.divider(style=inset_divider),

        gap="1rem",
        style=pl.style(max_width="600px", margin="0 auto", padding="2rem")
    )