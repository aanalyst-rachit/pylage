import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps



def get_app():
    return pl.column(
        pl.heading("PyLage UI Kit — Popover", level=1),
        pl.text("UI Kit Popover wrapper using the existing PyLage Popover component."),
        pl.heading("1. Basic Popover", level=3),
        pl.popover(
            pl.text("This is popover content."),
            title="Additional information",
            class_name="ui-kit-popover",
        ),
        pl.heading("2. Popover with Multiple Children", level=3),
        pl.popover(
            pl.card(
                pl.text("Popover details"),
                pl.button("Close"),
            ),
            title="Quick information",
        ),
        pl.heading("3. Props + Children", level=3),
        pl.popover(
            pl.text("Props and children are preserved by the UI Kit wrapper."),
            class_name="ui-kit-popover-demo",
            title="UI Kit Popover",
        ),
    )


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage UI Kit - Popover Manual Test", serve=True, host="0.0.0.0", port=3000)
