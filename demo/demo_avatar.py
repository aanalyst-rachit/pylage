import pylage as pl
import pylage as ps


def get_app():
    # Common shadow & style presets for avatars
    avatar_shadow = pl.style(
        box_shadow="0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
        border="2px solid #ffffff",
        transition="transform 0.2s ease"
    )

    return pl.column(
        ps.heading("Avatar"),
        ps.text("Semantic avatars with size and content composition."),

        # Default Avatar with shadow & border
        ps.avatar(
            "RK",
            style=avatar_shadow
        ),

        # Sizes pl.row with Shadow
        pl.row(
            ps.avatar("S", size="sm", style=avatar_shadow),
            ps.avatar("M", size="md", style=avatar_shadow),
            ps.avatar("L", size="lg", style=avatar_shadow),
            gap="1rem",
            style=pl.style(display="flex", align_items="center")
        ),

        # Image Avatar with Shadow & Ring Accent
        ps.avatar(
            pl.Image(src="https://i.pravatar.cc/100?img=33", alt="User"),
            style=pl.style(
                box_shadow="0 10px 15px -3px rgba(59, 130, 246, 0.3)", # Subtle colored glow
                border="2px solid #3b82f6"
            )
        ),

        # Custom Colored Avatar with Gradient & Elevation
        ps.avatar(
            "RK",
            size="lg",
            style=pl.style(
                background="linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)",
                color="#ffffff",
                box_shadow="0 10px 15px -3px rgba(29, 78, 216, 0.4)",
                font_weight="bold"
            ),
        ),
        gap="1.5rem",
        style=pl.style(max_width="600px", margin="0 auto", padding="2rem")
    )