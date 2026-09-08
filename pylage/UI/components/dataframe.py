from __future__ import annotations

from typing import Any

from pylage.ENGINE.components.basic import DataFrame as _DataFrame
from pylage.ENGINE.styling.style import Style


_DEFAULT_STYLE = Style(
    width="100%",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-lg)",
    overflow="hidden",
)


def dataframe(
    data: Any,
    *,
    headers: Any = None,
    style: Style | None = None,
    cell_border: bool = True,
    **props: Any,
):
    """Create an Excel-like DataFrame view.

    ``dataframe()`` is intentionally separate from ``table()``.
    """
    final_style = _DEFAULT_STYLE.merge(style)

    return _DataFrame(
        data=data,
        headers=headers,
        style=final_style,
        cell_border=cell_border,
        class_name=props.pop("class_name", "pylage-dataframe"),
        **props,
    )
