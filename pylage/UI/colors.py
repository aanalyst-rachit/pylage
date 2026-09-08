from __future__ import annotations

from typing import Any

from pylage.ENGINE.styling.global_theme import get_global_theme


class _ColorsFacade:
    def __getattr__(self, name: str) -> Any:
        theme = get_global_theme()
        if theme is None or name not in theme.colors:
            raise AttributeError(f"Unknown semantic color: {name}")
        return theme.colors[name]

    def __dir__(self) -> list[str]:
        theme = get_global_theme()
        if theme is None:
            return []
        return sorted(theme.colors.keys())


colors = _ColorsFacade()

__all__ = ["colors"]
