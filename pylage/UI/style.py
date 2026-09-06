from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.style import Style


class _StyleFacade:
    """Public style facade exposing presets and Style construction."""

    black = Style(
        background_color="#000000",
        color="#ffffff",
    )

    white = Style(
        background_color="#ffffff",
        color="#000000",
    )

    elevated_card = Style(
        box_shadow="0 10px 15px -3px rgba(0,0,0,0.1)",
    )

    topheader = Style(
        display="flex",
        align_items="center",
        justify_content="space-between",
        width="100%",
        padding="0.75rem 1.5rem",
    )

    def __call__(self, **properties: Any) -> Style:
        """Construct a Style using the public style API."""
        return Style(**properties)


style = _StyleFacade()


black = style.black
white = style.white
elevated_card = style.elevated_card
topheader = style.topheader


__all__ = [
    "style",
    "black",
    "white",
    "elevated_card",
    "topheader",
]
