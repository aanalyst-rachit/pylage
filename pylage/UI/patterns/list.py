"""List pattern for PyLage Layout."""

from typing import Any

from pylage.ENGINE.components import Column, Text


def List(*items: Any, **props: Any):
    """Create a reusable vertical list."""
    return Column(
        *(Text(item) for item in items),
        **props,
    )
