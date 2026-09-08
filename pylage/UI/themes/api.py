"""Public theme API for PyLage Layout."""

from pylage.ENGINE.styling.global_theme import get_global_theme, set_global_theme
from pylage.ENGINE.styling.theme import Theme

from .dark import DARK_THEME
from .light import LIGHT_THEME


_THEMES = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
}

# The public global theme starts with the light preset.
set_global_theme(LIGHT_THEME)


def get_theme(name: str) -> Theme:
    """Return a registered PyLage Layout theme by name."""
    try:
        return _THEMES[name]
    except KeyError:
        available = ", ".join(sorted(_THEMES))
        raise ValueError(
            f"Unknown theme: {name!r}. Available themes: {available}"
        ) from None


def set_theme(theme: str | Theme) -> None:
    """Set the process-wide active PyLage theme.

    Accepts either a registered theme name or a custom Theme instance.
    """
    if isinstance(theme, str):
        set_global_theme(get_theme(theme))
        return
    if isinstance(theme, Theme):
        set_global_theme(theme)
        return
    raise TypeError("theme must be a registered theme name or a Theme instance")


def get_current_theme() -> Theme:
    """Return the process-wide active PyLage theme."""
    theme = get_global_theme()
    if theme is None:
        return LIGHT_THEME
    return theme


def available_themes() -> tuple[str, ...]:
    """Return the names of all registered themes."""
    return tuple(sorted(_THEMES))


__all__ = [
    "DARK_THEME",
    "LIGHT_THEME",
    "available_themes",
    "get_current_theme",
    "get_theme",
    "set_theme",
]
