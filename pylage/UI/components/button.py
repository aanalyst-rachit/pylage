from __future__ import annotations

from typing import Any

from pylage.ENGINE import Button as _Button
from pylage.ENGINE import Style


_VARIANT_STYLES: dict[str, Style] = {
    "primary": Style(
        background_color="var(--color-primary)",
        color="var(--color-primary-contrast)",
        border='1px solid var(--color-primary)',
        pseudo={"hover": Style(background_color="var(--color-primary-hover)")},
    ),
    "secondary": Style(
        background_color="var(--color-secondary)",
        color="var(--color-secondary-contrast)",
        border='1px solid var(--color-secondary)',
        pseudo={"hover": Style(background_color="var(--color-secondary-hover)")},
    ),
    "outline": Style(
        background_color="var(--color-background)",
        color="var(--color-primary-hover)",
        border='1px solid var(--color-primary-hover)',
    ),
    "ghost": Style(
        background_color="transparent",
        color="var(--color-text)",
        border="1px solid transparent",
    ),
    "danger": Style(
        background_color="var(--color-danger)",
        color="var(--color-primary-contrast)",
        border='1px solid var(--color-danger)',
    ),
}

_SIZE_STYLES: dict[str, Style] = {
    "sm": Style(
        padding="0.5rem 0.75rem",
        font_size="0.875rem",
    ),
    "md": Style(
        padding="0.625rem 1rem",
        font_size="1rem",
    ),
    "lg": Style(
        padding="0.75rem 1.25rem",
        font_size="1.125rem",
    ),
}

_BASE_STYLE = Style(
    border_radius="var(--radius-lg)",
    font_weight="600",
    cursor="pointer",
)


_COMBINED_STYLES: dict[str, dict[str, Style]] = {
    variant: {
        size: _BASE_STYLE.merge(_VARIANT_STYLES[variant]).merge(
            _SIZE_STYLES[size]
        )
        for size in _SIZE_STYLES
    }
    for variant in _VARIANT_STYLES
}


def button(
    text: Any,
    *,
    variant: str = "primary",
    size: str = "md",
    bg: Style | None = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit button using the existing PyLage Button."""
    if variant not in _VARIANT_STYLES:
        valid = ", ".join(_VARIANT_STYLES)
        raise ValueError(
            f"Unknown button variant {variant!r}. "
            f"Expected one of: {valid}."
        )

    if size not in _SIZE_STYLES:
        valid = ", ".join(_SIZE_STYLES)
        raise ValueError(
            f"Unknown button size {size!r}. "
            f"Expected one of: {valid}."
        )

    default_style = _COMBINED_STYLES[variant][size]
    # ``bg`` is a public convenience API.  It accepts a Style
    # preset such as ``style.black`` and merges it before the
    # explicit ``style=`` override.
    if bg is not None and not isinstance(bg, Style):
        raise TypeError("bg must be a Style or None")

    final_style = default_style.merge(bg).merge(style)

    return _Button(text, style=final_style, **props)
