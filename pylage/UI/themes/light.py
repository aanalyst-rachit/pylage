"""Light theme preset for PyLage Layout."""

from ..tokens import COLORS
from .factory import create_theme

LIGHT_COLORS = {
    **COLORS,
}

LIGHT_THEME = create_theme(
    name="light",
    colors=LIGHT_COLORS,
)

__all__ = ["LIGHT_COLORS", "LIGHT_THEME"]
