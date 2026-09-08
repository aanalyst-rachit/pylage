"""Reusable statistics and metric patterns for PyLage Layout."""

from typing import Any, Iterable, Mapping

from pylage.ENGINE.components import Badge, Card, Column, Heading, Row, Text


def Metric(
    label: Any,
    value: Any,
    delta: Any = None,
    description: Any = None,
    **props: Any,
):
    """Streamlit/Reflex style Metric card.

    Displays a prominent key performance indicator with optional delta and label.
    Supports pylage.State for value and delta.
    """
    children = []

    # Value + Delta row
    val_comp = Heading(value, class_name="metric-value")
    if delta is not None:
        delta_str = str(getattr(delta, "value", delta))
        badge_variant = "success" if delta_str.startswith("+") else ("danger" if delta_str.startswith("-") else "secondary")
        delta_comp = Badge(Text(delta), variant=badge_variant, class_name="metric-delta")
        children.append(Row(val_comp, delta_comp, class_name="metric-value-row"))
    else:
        children.append(val_comp)

    # Label
    children.append(Text(label, class_name="metric-label"))

    # Optional description
    if description is not None:
        children.append(Text(description, class_name="metric-description"))

    return Card(
        *children,
        class_name=props.pop("class_name", "metric-card"),
        **props,
    )


# Alias
MetricCard = Metric


def StatsSection(
    title: str = "Stats",
    description: str | None = None,
    stats: Iterable[Any] = (),
    **props: Any,
):
    """Create a reusable statistics section using PyLage components.

    Each item in stats may be:
    - A Mapping with keys `value`, `label`, optional `description`, optional `delta`
    - A pre-built Component (like Metric(...))
    - A tuple of (label, value) or (label, value, delta)
    """
    cards = []

    for stat in stats:
        if hasattr(stat, "type"):
            cards.append(stat)
        elif isinstance(stat, Mapping):
            value = stat.get("value", "")
            label = stat.get("label", "")
            delta = stat.get("delta")
            stat_description = stat.get("description")
            cards.append(Metric(label=label, value=value, delta=delta, description=stat_description))
        elif isinstance(stat, (list, tuple)):
            label = stat[0] if len(stat) > 0 else ""
            value = stat[1] if len(stat) > 1 else ""
            delta = stat[2] if len(stat) > 2 else None
            cards.append(Metric(label=label, value=value, delta=delta))
        else:
            cards.append(Card(Text(str(stat))))

    content = [
        Heading(title),
    ]

    if description is not None:
        content.append(Text(description))

    content.append(Row(*cards))

    return Column(
        *content,
        class_name=props.pop("class_name", "stats-section"),
        **props,
    )
