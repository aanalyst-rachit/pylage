import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps



def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Tooltip", level=1),
        pl.text("UI Kit Tooltip wrapper using the existing PyLage Tooltip component."),
        pl.heading("1. pl.button Tooltip", level=3),
        pl.tooltip(
            pl.button("Hover target"),
            title="Helpful information",
            class_name="ui-kit-tooltip",
        ),
        pl.heading("2. pl.text Tooltip", level=3),
        pl.tooltip(
            pl.text("Hover over this information target"),
            title="This is a second tooltip",
        ),
    )


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage UI Kit - Tooltip Manual Test", serve=True, host="0.0.0.0", port=3000)
