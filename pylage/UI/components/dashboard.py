from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import Column as _Column
from pylage.ENGINE.components.basic import Heading as _Heading
from pylage.ENGINE.components.basic import Row as _Row

from pylage.UI.layout import Container, Stack
from .stat_group import stat_group


def dashboard(
    *,
    title: Any = None,
    header: Any = None,
    sidebar: Any = None,
    metrics: Any = None,
    stats: Any = None,
    filters: Any = None,
    content: Any = None,
    table: Any = None,
    footer: Any = None,
    **props: Any,
):
    """Compose a complete responsive dashboard page from PyLage UI primitives."""

    children: list[Any] = []

    if header is not None:
        children.append(header)

    body_children: list[Any] = []

    if sidebar is not None:
        body_children.append(sidebar)

    main_children: list[Any] = []

    if title is not None:
        if (
            isinstance(title, str)
            or hasattr(title, "value")
            or hasattr(title, "subscribe")
        ):
            main_children.append(
                _Heading(
                    title,
                    class_name="dashboard-title",
                )
            )
        else:
            main_children.append(title)

    effective_stats = metrics if metrics is not None else stats

    if effective_stats is not None:
        if isinstance(effective_stats, (list, tuple)):
            effective_stats = stat_group(*effective_stats)

        main_children.append(effective_stats)

    if filters is not None:
        if isinstance(filters, (list, tuple)):
            main_children.append(
                _Row(
                    *filters,
                    class_name="dashboard-filters-row",
                )
            )
        else:
            main_children.append(filters)

    if content is not None:
        main_children.append(content)

    if table is not None:
        main_children.append(table)

    main = _Column(
        *main_children,
        class_name="dashboard-main",
    )

    body_children.append(main)

    body = _Row(
        *body_children,
        class_name="dashboard-body",
    )

    children.append(body)

    if footer is not None:
        children.append(footer)

    return Container(
        Stack(
            *children,
            **props,
        )
    )
