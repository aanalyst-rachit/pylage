import pylage as pl
"""Manual demo for PyLage Media & Graphic components (Audio, Video, Canvas, Image, Icon)."""



def get_app() -> pl.column:
    is_playing_audio = pl.State(False)
    canvas_clicks = pl.State(0)

    title = pl.heading("🎨 Media & Graphic Components Manual", level=1)
    desc = pl.text(
        "Demonstrates Audio, Video, HTML5 Canvas, Image rendering, and Icon components in PyLage.",
        style=pl.style(color="#64748b", margin_bottom="1.5rem"),
    )

    # 1. Image Component
    img_card = pl.card(
        pl.heading("1. Image Component", level=3),
        pl.text("Responsive image with alt text and rounded border styling:"),
        pl.Image(
            src="https://images.unsplash.com/photo-1579546929518-9e396f3cc809?w=600&auto=format&fit=crop&q=80",
            alt="Gradient abstract artwork",
            width="100%",
            height="180px",
            style=pl.style(border_radius="0.5rem", object_fit="cover", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 2. Audio & Video Components
    media_card = pl.card(
        pl.heading("2. Audio & Video Elements", level=3),
        pl.text("Native multimedia controls integrated directly into the reactive tree:"),
        pl.row(
            pl.column(
                pl.heading("Audio Player", level=4),
                pl.Audio(
                    src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
                    controls=True,
                    style=pl.style(width="100%", margin_top="0.5rem"),
                ),
                style=pl.style(flex="1"),
            ),
            pl.column(
                pl.heading("Video Player", level=4),
                pl.Video(
                    src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                    controls=True,
                    width="100%",
                    height="160px",
                    style=pl.style(border_radius="0.5rem", margin_top="0.5rem"),
                ),
                style=pl.style(flex="1"),
            ),
            style=pl.style(gap="1.5rem", margin_top="0.75rem"),
        ),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    # 3. Canvas & Icon
    def handle_canvas_click():
        canvas_clicks.set(canvas_clicks.value + 1)

    canvas_card = pl.card(
        pl.heading("3. Canvas & Icon Visuals", level=3),
        pl.text("Interactive Canvas element with reactive click tracking:"),
        pl.row(
            pl.Icon(name="activity", size="24", color="#3b82f6"),
            pl.text("Canvas Click Count: "),
            pl.text(canvas_clicks, style=pl.style(font_weight="bold", color="#3b82f6")),
            style=pl.style(align_items="center", gap="0.5rem", margin_bottom="0.75rem"),
        ),
        pl.Canvas(
            width="400",
            height="100",
            on_click=handle_canvas_click,
            style=pl.style(
                background="#f8fafc",
                border="2px dashed #cbd5e1",
                border_radius="0.5rem",
                width="100%",
                cursor="pointer",
            ),
        ),
        pl.text("Click the canvas area above to trigger reactive state updates.", style=pl.style(font_size="0.875rem", color="#94a3b8", margin_top="0.5rem")),
        style=pl.style(padding="1.25rem", margin_bottom="1rem", background="#ffffff", border="1px solid #e2e8f0", border_radius="0.75rem"),
    )

    return pl.column(
        title,
        desc,
        img_card,
        media_card,
        canvas_card,
        style=pl.style(padding="2rem", max_width="900px", margin="0 auto"),
    )
