from __future__ import annotations

from typing import Any

from pylage.ENGINE import Label, Style
from pylage.UI.components.text import text
from pylage.UI.layout.factories import Stack


def form_field(
    child: Any,
    *,
    label: Any = None,
    help_text: Any = None,
    error: Any = None,
    required: bool = False,
    style: Style | None = None,
    **props: Any,
):
    """Create a semantic form field around an existing input control.

    FormField is a composition component. It does not introduce a new
    renderer or input implementation; it arranges an existing control
    together with its label, help text, and error presentation.
    """

    children: list[Any] = []

    if label is not None:
        control_id = child.props.get("id")
        if control_id is None:
            control_id = f"pylage-field-{child.id}"
            child.props["id"] = control_id
        label_value = f"{label} *" if required else label
        children.append(Label(label_value, **{"for": control_id}))

    if required:
        child.props.setdefault("required", True)

    children.append(child)

    described_by: list[str] = []

    existing_described_by = child.props.get("aria-describedby")
    if existing_described_by:
        described_by.extend(str(existing_described_by).split())

    if help_text is not None:
        help_id = f"pylage-field-help-{child.id}"
        children.append(
            text(
                help_text,
                muted=True,
                caption=True,
                id=help_id,
            )
        )
        described_by.append(help_id)

    if error is not None:
        error_id = f"pylage-field-error-{child.id}"
        children.append(text(error, id=error_id))
        described_by.append(error_id)
        child.props["aria-invalid"] = "true"

    if described_by:
        child.props["aria-describedby"] = " ".join(dict.fromkeys(described_by))

    return Stack(
        *children,
        style=style,
        **props,
    )


__all__ = ["form_field"]
