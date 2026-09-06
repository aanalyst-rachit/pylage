from __future__ import annotations

from typing import Any, Mapping
from pylage.ENGINE import Grid as _Grid
from pylage.ENGINE import Style
from .metric import metric as _metric

_DEFAULT_GRID_STYLE = Style(
    display="grid",
    width="100%",
    gap="var(--spacing-lg)",
)

def stat_group(
    *stats: Any,
    items: list[Any] | None = None,
    columns: int | str = "repeat(auto-fit, minmax(240px, 1fr))",
    style: Style | None = None,
    **props: Any,
):
    """Create a cohesive, responsive grid of metric cards."""
    all_stats: list[Any] = []
    if stats:
        all_stats.extend(stats)
    if items:
        all_stats.extend(items)

    metric_cards: list[Any] = []
    for item in all_stats:
        if hasattr(item, "type"):
            metric_cards.append(item)
        elif isinstance(item, Mapping):
            metric_cards.append(_metric(**item))
        elif isinstance(item, (list, tuple)):
            label = item[0] if len(item) > 0 else ""
            value = item[1] if len(item) > 1 else ""
            delta = item[2] if len(item) > 2 else None
            desc = item[3] if len(item) > 3 else None
            metric_cards.append(_metric(label=label, value=value, delta=delta, description=desc))
        else:
            metric_cards.append(item)

    cols_str = (
        f"repeat({columns}, minmax(0, 1fr))"
        if isinstance(columns, int)
        else str(columns)
    )

    base_style = _DEFAULT_GRID_STYLE.merge(
        Style(grid_template_columns=cols_str)
    )
    final_style = base_style.merge(style)

    return _Grid(
        *metric_cards,
        style=final_style,
        **props,
    )
