from __future__ import annotations

from typing import Any
from pylage.ENGINE.styling.style import Style
from .stat_group import stat_group

def metric_grid(
    *metrics: Any,
    items: list[Any] | None = None,
    columns: int | str = "repeat(auto-fit, minmax(240px, 1fr))",
    style: Style | None = None,
    **props: Any,
):
    """Create a responsive grid of KPI metrics."""
    return stat_group(
        *metrics,
        items=items,
        columns=columns,
        style=style,
        **props,
    )
