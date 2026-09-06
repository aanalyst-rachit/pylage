from __future__ import annotations

from typing import Any

from pylage.ENGINE import Style
from pylage.ENGINE import Table as _Table


_DEFAULT_STYLE = Style(
    width="100%",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-lg)",
    overflow="hidden",
)


def table(
    data: Any = None,
    *,
    headers: Any = None,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic UI Kit table using the existing PyLage Table."""
    final_style = _DEFAULT_STYLE.merge(style)

    return _Table(
        data=data,
        headers=headers,
        style=final_style,
        **props,
    )
