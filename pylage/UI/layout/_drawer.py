from __future__ import annotations

from typing import Any

BREAKPOINTS = ("base", "sm", "md", "lg", "xl")
MODES = {"overlay", "persistent"}


def normalize_responsive_mode(value: dict[str, Any]) -> dict[str, str]:
    """Validate and normalize responsive Drawer modes."""
    if not isinstance(value, dict) or not value:
        raise ValueError(
            "responsive_mode must be a non-empty mapping"
        )

    normalized: dict[str, str] = {}

    for breakpoint, mode in value.items():
        if breakpoint not in BREAKPOINTS:
            raise ValueError(
                "responsive_mode breakpoints must be one of: "
                "base, sm, md, lg, xl"
            )
        if mode not in MODES:
            raise ValueError(
                "responsive_mode values must be one of: "
                "overlay, persistent"
            )
        normalized[breakpoint] = mode

    if "base" not in normalized:
        normalized["base"] = "overlay"

    return {
        breakpoint: normalized[breakpoint]
        for breakpoint in BREAKPOINTS
        if breakpoint in normalized
    }
