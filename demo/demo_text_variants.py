from __future__ import annotations

import pylage as pl

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))



def get_app():
    return pl.column(
        pl.heading("Surface Components"),
        pl.text("Primary body text"),
        pl.text("Secondary information", muted=True),
        pl.text("Field label", label=True),
        pl.text("Small metadata", caption=True),
    )
