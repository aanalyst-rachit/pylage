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
    "primary": "#2563eb",
    "primary_hover": "#1d4ed8",
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



def _normalize_hex_color(value: str) -> str:
    """Normalize a CSS hexadecimal color to six lowercase digits."""
    if not isinstance(value, str):
        raise TypeError('color must be a string')

    color = value.strip().lstrip('#')

    if len(color) == 3:
        color = ''.join(character * 2 for character in color)

    if len(color) != 6 or any(
        character not in '0123456789abcdefABCDEF'
        for character in color
    ):
        raise ValueError('color must be a valid 3 or 6 digit hexadecimal value')

    return color.lower()


def _relative_luminance(color: str) -> float:
    """Return the WCAG relative luminance of a hexadecimal color."""
    normalized = _normalize_hex_color(color)

    channels = [
        int(normalized[index:index + 2], 16) / 255
        for index in range(0, 6, 2)
    ]

    linear = [
        channel / 12.92
        if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]

    return (
        0.2126 * linear[0]
        + 0.7152 * linear[1]
        + 0.0722 * linear[2]
    )


def contrast_ratio(foreground: str, background: str) -> float:
    """Return the numeric WCAG contrast ratio between two hex colors."""
    foreground_luminance = _relative_luminance(foreground)
    background_luminance = _relative_luminance(background)

    lighter = max(foreground_luminance, background_luminance)
    darker = min(foreground_luminance, background_luminance)

    return (lighter + 0.05) / (darker + 0.05)


def meets_wcag_contrast(
    foreground: str,
    background: str,
    *,
    level: str = 'AA',
    large_text: bool = False,
) -> bool:
    """Return whether a color pair satisfies the requested WCAG threshold."""
    normalized_level = str(level).upper()

    if normalized_level not in {'AA', 'AAA'}:
        raise ValueError('level must be AA or AAA')

    thresholds = {
        ('AA', False): 4.5,
        ('AA', True): 3.0,
        ('AAA', False): 7.0,
        ('AAA', True): 4.5,
    }

    return contrast_ratio(foreground, background) >= thresholds[
        (normalized_level, bool(large_text))
    ]


def theme_contrast_results(
    colors: dict[str, str] | None = None,
) -> dict[str, float]:
    """Return numeric contrast ratios for the primary theme color pairs."""
    palette = COLORS if colors is None else colors

    required_pairs = {
        'text_on_background': ('text', 'background'),
        'text_on_surface': ('text', 'surface'),
        'muted_text_on_background': ('text_muted', 'background'),
        'primary_contrast': ('primary_contrast', 'primary'),
        'secondary_contrast': ('secondary_contrast', 'secondary'),
    }

    results = {}

    for name, (foreground_key, background_key) in required_pairs.items():
        results[name] = contrast_ratio(
            palette[foreground_key],
            palette[background_key],
        )

    return results


def validate_wcag_contrast(
    colors: dict[str, str] | None = None,
) -> bool:
    """Validate the core theme color pairs against WCAG AA thresholds."""
    palette = COLORS if colors is None else colors

    required_checks = (
        ('text', 'background', False),
        ('text', 'surface', False),
        ('text_muted', 'background', False),
        ('primary_contrast', 'primary', False),
        ('secondary_contrast', 'secondary', False),
    )

    return all(
        meets_wcag_contrast(
            palette[foreground],
            palette[background],
            level='AA',
            large_text=large_text,
        )
        for foreground, background, large_text in required_checks
    )


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
    "contrast_ratio",
    "meets_wcag_contrast",
    "theme_contrast_results",
    "validate_wcag_contrast",
]
