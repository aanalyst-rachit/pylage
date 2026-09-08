"""Reusable UI Kit modal recipe."""

from __future__ import annotations

from typing import Any

from pylage.UI.components.card import card
from pylage.UI.components.dialog import dialog
from pylage.ENGINE.styling.style import Style

__all__ = ["modal"]


_BASE_STYLE = Style(
    padding="var(--spacing-lg)",
)


def modal(
    content: Any,
    *,
    open: Any = False,
    title: Any = None,
    style: Style | None = None,
    **props: Any,
):
    """Compose a reusable modal from the existing UI Kit dialog and card."""

    children = []

    if title is not None:
        children.append(title)

    children.append(content)

    content_card = card(
        *children,
        style=_BASE_STYLE.merge(style),
    )

    return dialog(
        content_card,
        open=open,
        **props,
    )
