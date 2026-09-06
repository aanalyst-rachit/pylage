"""Reusable UI Kit loading overlay recipe."""

from __future__ import annotations

from typing import Any

from pylage.ENGINE import Spinner as _Spinner
from pylage.ENGINE import Style
from pylage.ENGINE import Text as _Text
from pylage.UI.components.dialog import dialog
from pylage.UI.layout.column import column

__all__ = ["loading_overlay"]

_OVERLAY_STYLE = Style(
    position="fixed",
    top=0,
    right=0,
    bottom=0,
    left=0,
    width="100vw",
    height="100vh",
    max_width="none",
    max_height="none",
    margin=0,
    padding=0,
    box_sizing="border-box",
    background_color="rgba(0, 0, 0, 0.45)",
    border="none",
    border_radius=0,
    z_index=1100,
    color="var(--color-text)",
)

_CONTENT_STYLE = Style(
    width="100vw",
    height="100vh",
    box_sizing="border-box",
    display="flex",
    flex_direction="column",
    align_items="center",
    justify_content="center",
    gap="var(--spacing-sm)",
    padding="var(--spacing-lg)",
    text_align="center",
)

_TEXT_STYLE = Style(
    font_size="1rem",
    font_weight="500",
    color="var(--color-text)",
    margin="0",
)


def loading_overlay(
    text: Any = "Loading...",
    *,
    open: Any = False,
    spinner: bool = True,
    style: Style | None = None,
    **props: Any,
):
    """Create a blocking, full-viewport loading overlay using the existing Dialog."""
    items: list[Any] = []

    if spinner:
        items.append(_Spinner())

    if text is not None:
        items.append(_Text(text, style=_TEXT_STYLE))

    content = column(*items, style=_CONTENT_STYLE)
    final_style = _OVERLAY_STYLE.merge(style)

    return dialog(
        content,
        open=open,
        style=final_style,
        **props,
    )
