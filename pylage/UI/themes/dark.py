"""Dark theme preset for PyLage Layout."""

from .factory import create_theme


DARK_COLORS = {
    "background": "#0f172a",
    "surface": "#1e293b",
    "surface_variant": "#334155",
    "text": "#f8fafc",
    "text_muted": "#94a3b8",
    "border": "#475569",
    "border_muted": "#64748b",
    "primary": "#60a5fa",
    "primary_hover": "#3b82f6",
    "primary_contrast": "#0f172a",
    "secondary": "#94a3b8",
    "secondary_hover": "#64748b",
    "secondary_contrast": "#0f172a",
    "success": "#4ade80",
    "warning": "#fbbf24",
    "danger": "#f87171",
    "danger_bg": "#450a0a",
    "danger_border": "#7f1d1d",
    "info": "#38bdf8",
}

DARK_THEME = create_theme(
    name="dark",
    colors=DARK_COLORS,
)

__all__ = ["DARK_COLORS", "DARK_THEME"]
