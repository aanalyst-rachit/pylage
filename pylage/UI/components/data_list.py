from __future__ import annotations

from typing import Any, Mapping
from pylage.ENGINE import Column as _Column
from pylage.ENGINE import Row as _Row
from pylage.ENGINE import Style
from pylage.ENGINE import Text as _Text

_DEFAULT_CONTAINER_STYLE = Style(
    display="flex",
    flex_direction="column",
    width="100%",
    background_color="var(--color-background)",
    border="1px solid var(--color-border)",
    border_radius="var(--radius-xl)",
    padding="var(--spacing-md)",
    gap="var(--spacing-sm)",
)

_LABEL_STYLE = Style(
    font_size="0.875rem",
    font_weight="500",
    color="var(--color-text-muted)",
    margin="0",
)

_VALUE_STYLE = Style(
    font_size="0.875rem",
    font_weight="500",
    color="var(--color-text)",
    margin="0",
)

_ROW_HORIZONTAL_STYLE = Style(
    display="flex",
    flex_direction="row",
    justify_content="space-between",
    align_items="center",
    padding="var(--spacing-xs) 0",
    width="100%",
)

_ROW_DIVIDED_STYLE = Style(
    border_bottom="1px solid var(--color-border-muted)",
    padding_bottom="var(--spacing-sm)",
)

def data_list(
    data: Mapping[str, Any] | list[tuple[Any, Any]] | list[Mapping[str, Any]],
    *,
    orientation: str = "horizontal",
    divided: bool = True,
    style: Style | None = None,
    **props: Any,
):
    """Create a high-level key-value data list component."""
    items: list[tuple[Any, Any]] = []

    if isinstance(data, Mapping):
        items = list(data.items())
    elif isinstance(data, (list, tuple)):
        for entry in data:
            if isinstance(entry, Mapping):
                label = entry.get("label", "")
                val = entry.get("value", "")
                items.append((label, val))
            elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
                items.append((entry[0], entry[1]))
            else:
                items.append(("", entry))

    rows: list[Any] = []
    total = len(items)

    for idx, (lbl, val) in enumerate(items):
        is_last = (idx == total - 1)

        lbl_comp = lbl if hasattr(lbl, "type") else _Text(lbl, style=_LABEL_STYLE)
        val_comp = val if hasattr(val, "type") else _Text(val, style=_VALUE_STYLE)

        row_style = _ROW_HORIZONTAL_STYLE
        if divided and not is_last:
            row_style = row_style.merge(_ROW_DIVIDED_STYLE)

        if orientation == "vertical":
            col_style = Style(
                display="flex",
                flex_direction="column",
                gap="0.25rem",
                width="100%",
                padding="var(--spacing-xs) 0",
            )
            if divided and not is_last:
                col_style = col_style.merge(_ROW_DIVIDED_STYLE)
            rows.append(_Column(lbl_comp, val_comp, style=col_style))
        else:
            rows.append(_Row(lbl_comp, val_comp, style=row_style))

    final_style = _DEFAULT_CONTAINER_STYLE.merge(style)

    return _Column(
        *rows,
        style=final_style,
        **props,
    )
