import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps




def get_app():
    loading = pl.state(False)
    status = pl.state("Overlay is hidden.")

    def toggle_loading(e=None):
        print("CLICK RECEIVED:", e)
        print("LOADING BEFORE:", loading.value)
        next_value = not loading.value
        loading.set(next_value)
        status.set("Loading overlay is visible." if next_value else "Overlay is hidden.")
        print("LOADING AFTER:", loading.value)
        print("STATUS AFTER:", status.value)

    content = pl.column(
        pl.heading("Loading Overlay Manual Test", level=2),
        pl.text("This page verifies the UI Kit pl.loading_overlay() recipe."),
        pl.text(status, style=pl.style(font_weight="bold")),
        pl.button(
            "Start / Stop Loading",
            on_click=toggle_loading,
            variant="primary",
        ),
        pl.text("Click the button to show the full-viewport loading overlay. Click again to hide it."),
        style=pl.style(
            display="flex",
            flex_direction="column",
            gap="1rem",
            padding="2rem",
            min_height="400px",
        ),
    )

    overlay = pl.loading_overlay(
        "Please wait...",
        open=loading,
        spinner=True,
        title="Loading overlay",
    )

    app = pl.column(
        content,
        pl.card(
            pl.text("Underlying page content remains mounted while the overlay is toggled."),
            style=pl.style(padding="1.5rem", margin_top="1rem"),
        ),
        overlay,
        style=pl.style(
            display="flex",
            flex_direction="column",
            gap="1.5rem",
            padding="2rem",
            font_family="system-ui, sans-serif",
        ),
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage UI Kit Loading Overlay Manual", serve=True, host="0.0.0.0", port=3000)
