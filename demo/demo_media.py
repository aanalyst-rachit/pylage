import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps

def get_app():
    # pl.State tracking for interactive canvas/media status
    media_status = pl.State("Status: Media components ready")

    def handle_media_click():
        media_status.set("⚡ Media component clicked!")

    # ============================================================
    # 1. IMAGE COMPONENT
    # ============================================================
    image_section = pl.column(
        pl.text("1. Image Component", style=pl.style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        pl.Image(
            src="https://picsum.photos/600/200",
            alt="Sample Placeholder Image",
            style=pl.style(
                width="100%",
                height="150px",
                border_radius="0.5rem",
                border="1px solid #cbd5e1",
            ),
        ),
    )

    # ============================================================
    # 2. VIDEO COMPONENT
    # ============================================================
    video_section = pl.column(
        pl.text("2. Video Component", style=pl.style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        pl.Video(
            src="https://www.w3schools.com/html/mov_bbb.mp4",
            controls=True,
            style=pl.style(
                width="100%",
                max_height="220px",
                border_radius="0.5rem",
                background_color="#000000",
            ),
        ),
    )

    # ============================================================
    # 3. AUDIO COMPONENT
    # ============================================================
    audio_section = pl.column(
        pl.text("3. Audio Component", style=pl.style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        pl.Audio(
            src="https://www.w3schools.com/html/horse.mp3",
            controls=True,
            style=pl.style(width="100%"),
        ),
    )

    # ============================================================
    # 4. ICON & AVATAR (HORIZONTAL DIVIDER DEMO)
    # ============================================================
    icon_avatar_section = pl.column(
        pl.text("4. Icon & pl.avatar (Side-by-Side with Vertical pl.divider)", style=pl.style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        pl.row(
            # Icon Demo (Fixed: Using name="...")
            pl.column(
                pl.text("Icons", style=pl.style(font_weight="600", font_size="0.9rem", margin_bottom="0.25rem")),
                pl.row(
                    pl.Icon(name="check", style=pl.style(color="#166534", font_size="1.5rem")),
                    pl.Icon(name="star", style=pl.style(color="#d97706", font_size="1.5rem")),
                    pl.Icon(name="user", style=pl.style(color="#2563eb", font_size="1.5rem")),
                    style=pl.style(gap="0.75rem", align_items="center"),
                ),
            ),

            # VERTICAL DIVIDER
            pl.divider(
                orientation="vertical",
                style=pl.style(height="50px", border="1px solid #cbd5e1", margin="0 1rem"),
            ),

            # pl.avatar Demo
            pl.column(
                pl.text("Avatars", style=pl.style(font_weight="600", font_size="0.9rem", margin_bottom="0.25rem")),
                pl.row(
                    pl.avatar(
                        src="https://i.pravatar.cc/100?img=33",
                        name="Rachit Kumar",
                        style=pl.style(width="40px", height="40px", border_radius="999px"),
                    ),
                    pl.avatar(
                        name="User Fallback",
                        style=pl.style(width="40px", height="40px", border_radius="999px", background_color="#2563eb", color="#ffffff"),
                    ),
                    style=pl.style(gap="0.75rem", align_items="center"),
                ),
            ),
            style=pl.style(align_items="center", padding="1rem", background_color="#ffffff", border="1px solid #e2e8f0", border_radius="0.5rem"),
        ),
    )

    # ============================================================
    # 5. CANVAS COMPONENT
    # ============================================================
    canvas_section = pl.column(
        pl.text("5. Canvas Component (Interactive Render)", style=pl.style(font_weight="700", font_size="1.1rem", margin_bottom="0.5rem")),
        pl.Canvas(
            width=500,
            height=120,
            on_click=handle_media_click,
            style=pl.style(
                width="100%",
                height="120px",
                background_color="#f1f5f9",
                border="1px dashed #2563eb",
                border_radius="0.5rem",
                cursor="pointer",
            ),
        ),
    )

    # Horizontal pl.divider Helper
    def create_horizontal_divider():
        return pl.divider(
            orientation="horizontal",
            style=pl.style(
                width="100%",
                border="1px solid #e2e8f0",
                margin="1.5rem 0",
            ),
        )

    # ============================================================
    # MAIN APP STRUCTURE
    # ============================================================
    return pl.column(
        pl.heading(
            "PyLage Media — Live Manual",
            style=pl.style(font_size="1.75rem", font_weight="700", color="#0f172a", margin_bottom="0.5rem"),
        ),
        pl.text(
            "Media components (Image, Video, Audio, Icon, Canvas, pl.avatar) with Horizontal & Vertical Dividers:",
            style=pl.style(color="#64748b", margin_bottom="1rem"),
        ),

        pl.text(media_status, style=pl.style(color="#166534", font_weight="600", margin_bottom="1rem")),

        image_section,
        create_horizontal_divider(),

        video_section,
        create_horizontal_divider(),

        audio_section,
        create_horizontal_divider(),

        icon_avatar_section,
        create_horizontal_divider(),

        canvas_section,

        style=pl.style(
            width="100%",
            max_width="750px",
            min_height="100vh",
            padding="2rem",
            background_color="#f8fafc",
            box_sizing="border-box",
        ),
    )
