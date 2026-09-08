"""Reusable UI Kit confirmation dialog recipe."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.style import Style
from pylage.UI.components.dialog import dialog
from pylage.UI.components.button import button
from pylage.UI.layout.row import row

__all__ = ["confirmation_dialog"]


_ACTIONS_STYLE = Style(
    display="flex",
    justify_content="flex-end",
    gap="var(--spacing-sm)",
    margin_top="var(--spacing-lg)",
)


def confirmation_dialog(
    message: Any,
    *,
    title: Any = None,
    open: Any = False,
    on_confirm: Any = None,
    on_cancel: Any = None,
    confirm_text: Any = "Confirm",
    cancel_text: Any = "Cancel",
    confirm_variant: str = "primary",
    style: Style | None = None,
    **props: Any,
):
    """Compose a reusable confirmation flow from existing UI Kit primitives."""
    content = []

    if title is not None:
        content.append(title)

    if message is not None:
        content.append(message)

    cancel_props = {}
    if on_cancel is not None:
        cancel_props["on_click"] = on_cancel

    confirm_props = {}
    if on_confirm is not None:
        confirm_props["on_click"] = on_confirm

    actions = row(
        button(cancel_text, variant="secondary", **cancel_props),
        button(confirm_text, variant=confirm_variant, **confirm_props),
        style=_ACTIONS_STYLE,
    )

    content.append(actions)

    return dialog(
        *content,
        open=open,
        style=style,
        **props,
    )
