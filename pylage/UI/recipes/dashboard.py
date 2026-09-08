"""Dashboard page template for PyLage Layout."""

from typing import Any

from ..layout import Container, Stack
from pylage.ENGINE.components import Column, Heading, Row


def Dashboard(
    header: Any = None,
    sidebar: Any = None,
    content: Any = None,
    stats: Any = None,
    table: Any = None,
    footer: Any = None,
    title: Any = None,
    metrics: Any = None,
    filters: Any = None,
    **props: Any,
):
    """Compose a dashboard page from existing PyLage Layout primitives.

    Accepts Streamlit/Reflex style slot arguments:
    - title: Dashboard heading (str, State, or Component)
    - metrics / stats: Key metrics or stats row/cards
    - filters: Filter bar or interactive controls
    - table: Data table or primary visualizer
    - content: Main content or additional components
    - sidebar: Navigation or filter sidebar
    - header / footer: Page header and footer
    """
    children = []

    if header is not None:
        children.append(header)

    body_children = []

    if sidebar is not None:
        body_children.append(sidebar)

    main_children = []

    if title is not None:
        if isinstance(title, str) or hasattr(title, "value") or hasattr(title, "subscribe"):
            main_children.append(Heading(title, class_name="dashboard-title"))
        else:
            main_children.append(title)

    effective_stats = metrics if metrics is not None else stats
    if effective_stats is not None:
        if isinstance(effective_stats, (list, tuple)):
            main_children.append(Row(*effective_stats, class_name="dashboard-metrics-row"))
        else:
            main_children.append(effective_stats)

    if filters is not None:
        if isinstance(filters, (list, tuple)):
            main_children.append(Row(*filters, class_name="dashboard-filters-row"))
        else:
            main_children.append(filters)

    if content is not None:
        main_children.append(content)

    if table is not None:
        main_children.append(table)

    main = Column(
        *main_children,
        class_name="dashboard-main",
    )

    body_children.append(main)

    body = Row(
        *body_children,
        class_name="dashboard-body",
    )

    children.append(body)

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(*children, **props)
    )
