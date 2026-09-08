import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    current_slide = pl.state(0)
    slide_title = pl.state("Slide 1: Lightning Fast Diff")

    slides_info = [
        "Slide 1: Lightning Fast Diff Engine",
        "Slide 2: Pure Python Component Tree",
        "Slide 3: Reactive pl.State Binding & Batching",
    ]

    def next_slide(e=None):
        new_idx = (current_slide.value + 1) % len(slides_info)
        current_slide.set(new_idx)
        slide_title.set(slides_info[new_idx])

    def prev_slide(e=None):
        new_idx = (current_slide.value - 1) % len(slides_info)
        current_slide.set(new_idx)
        slide_title.set(slides_info[new_idx])

    # Slide Cards
    slide_1 = pl.card(
        pl.heading("Slide 1", level=3),
        pl.text("PyLage diff engine operates with sub-millisecond overhead per state change."),
        style=pl.style(padding="2rem", background="#eff6ff", border="1px solid #bfdbfe", border_radius="12px")
    )

    slide_2 = pl.card(
        pl.heading("Slide 2", level=3),
        pl.text("No JSX or client-side JavaScript authored — 100% Pythonic syntax."),
        style=pl.style(padding="2rem", background="#f0fdf4", border="1px solid #bbf7d0", border_radius="12px")
    )

    slide_3 = pl.card(
        pl.heading("Slide 3", level=3),
        pl.text("Coalesced scheduler queues prevent DOM thrashing on rapid mutations."),
        style=pl.style(padding="2rem", background="#faf5ff", border="1px solid #e9d5ff", border_radius="12px")
    )

    carousel_node = pl.carousel(
        slide_1,
        slide_2,
        slide_3,
        class_name="pylage-carousel",
        title="PyLage Feature Carousel",
        style=pl.style(width="100%", max_width="600px")
    )

    # Controls
    controls = pl.row(
        pl.button("◀ Previous Slide", on_click=prev_slide, variant="secondary"),
        pl.button("Next Slide ▶", on_click=next_slide, variant="primary"),
        style=pl.style(display="flex", gap="1rem", justify_content="center", margin_top="1rem")
    )

    app = pl.column(
        pl.heading("Carousel Component — Live Manual Test Suite", level=1),
        pl.text("Test slide index cycling, previous/next triggers, and state synchronization."),
        pl.card(
            pl.row(
                pl.text("Active Slide Index: ", style=pl.style(font_weight="bold")),
                pl.heading(current_slide, level=3, style=pl.style(color="#2563eb", margin="0")),
                pl.text(" | ", style=pl.style(margin="0 0.5rem", color="#94a3b8")),
                pl.text(slide_title, style=pl.style(font_weight="bold", color="#1e293b")),
                style=pl.style(display="flex", align_items="center")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        carousel_node,
        controls,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage Carousel Manual Test", serve=True, host="0.0.0.0", port=3000)
