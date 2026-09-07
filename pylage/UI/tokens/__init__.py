"""Design tokens for PyLage Layout."""

from typing import Any

COLORS: dict[str, str] = {
    "background": "#ffffff",
    "surface": "#f8fafc",
    "surface_variant": "#f1f5f9",
    "text": "#0f172a",
    "text_muted": "#64748b",
    "border": "#e2e8f0",
    "border_muted": "#cbd5e1",
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "primary_contrast": "#ffffff",
    "secondary": "#64748b",
    "secondary_hover": "#475569",
    "secondary_contrast": "#ffffff",
    "success": "#22c55e",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "danger_bg": "#fef2f2",
    "danger_border": "#fecaca",
    "info": "#06b6d4",
}

FONTS: dict[str, str] = {
    "sans": "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "serif": "Georgia, Cambria, 'Times New Roman', Times, serif",
    "mono": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
}

RADIUS: dict[str, str] = {
    "none": "0px",
    "sm": "0.125rem",
    "md": "0.375rem",
    "lg": "0.5rem",
    "xl": "0.75rem",
    "2xl": "1rem",
    "full": "9999px",
}

SPACING: dict[str, str] = {
    "0": "0px",
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "2xl": "3rem",
    "3xl": "4rem",
    "4xl": "6rem",
}


def validate_tokens() -> bool:
    """Validate all token registries for required keys and formats."""
    required_colors = {
        "background", "surface", "surface_variant",
        "text", "text_muted",
        "border", "border_muted",
        "primary", "primary_hover", "primary_contrast",
        "secondary", "secondary_hover", "secondary_contrast",
        "success", "warning",
        "danger", "danger_bg", "danger_border",
        "info",
    }
    if not required_colors.issubset(COLORS.keys()):
        return False

    required_fonts = {"sans", "serif", "mono"}
    if not required_fonts.issubset(FONTS.keys()):
        return False

    required_radius = {"none", "sm", "md", "lg", "xl", "2xl", "full"}
    if not required_radius.issubset(RADIUS.keys()):
        return False

    required_spacing = {"0", "xs", "sm", "md", "lg", "xl", "2xl", "3xl", "4xl"}
    if not required_spacing.issubset(SPACING.keys()):
        return False

    return True


__all__ = [
    "COLORS",
    "FONTS",
    "RADIUS",
    "SPACING",
    "validate_tokens",
]
