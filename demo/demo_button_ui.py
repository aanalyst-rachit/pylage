import pylage as pl
import sys
from pathlib import Path

# Ensure local pylage import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps
import pylage as ui


def get_app():
    return pl.column(
        pl.heading(
            "PyLage UI Kit — Button",
            level=2,
        ),
        pl.text(
            "Semantic Button API using the existing PyLage engine."
        ),
        ui.button("Primary"),
        ui.button("Secondary", variant="secondary"),
        ui.button("Outline", variant="outline"),
        ui.button("Ghost", variant="ghost"),
        ui.button("Danger", variant="danger"),
        ui.button("Small", size="sm"),
        ui.button("Medium", size="md"),
        ui.button("Large", size="lg"),
        ui.button(
            "Disabled",
            disabled=True,
            style=pl.style(opacity="0.6"),
        ),
    )
