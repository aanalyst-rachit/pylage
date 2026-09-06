from __future__ import annotations

from typing import Any
from pylage.ENGINE import Grid as _Grid
from pylage.ENGINE import Style

_DEFAULT_GRID_STYLE = Style(
    display="grid",
    width="100%",
    gap="var(--spacing-xl)",
)

_PRESETS: dict[str, str] = {
    "auto": "repeat(auto-fit, minmax(340px, 1fr))",
    "2-col": "repeat(2, minmax(0, 1fr))",
    "3-col": "repeat(3, minmax(0, 1fr))",
    "main-side": "2fr 1fr",
    "side-main": "1fr 2fr",
}

def dashboard_grid(
    *widgets: Any,
    layout: str = "auto",
    columns: int | str | None = None,
    gap: str | None = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a high-level responsive grid container for dashboard widgets."""
    if columns is not None:
        if isinstance(columns, int):
            cols_str = f"repeat({columns}, minmax(0, 1fr))"
        else:
            cols_str = str(columns)
    else:
        cols_str = _PRESETS.get(layout, _PRESETS["auto"])

    grid_style = Style(grid_template_columns=cols_str)
    if gap is not None:
        grid_style = grid_style.merge(Style(gap=gap))

    final_style = _DEFAULT_GRID_STYLE.merge(grid_style).merge(style)

    return _Grid(
        *widgets,
        style=final_style,
        **props,
    )
