import pylage as pl
import pylage as ps



def get_app():
    terms = pl.State(False)
    notifications = pl.State(True)
    custom_checked = pl.State(False)
    status = pl.State("Not changed yet")

    def handle_custom_change(payload):
        checked = payload.get("checked", False) if isinstance(payload, dict) else bool(payload)
        custom_checked.set(checked)
        status.set(f"Custom handler: {checked}")

    basic_checkbox = ps.checkbox(
        name="terms-basic",
        checked=False,
        title="Basic checkbox",
    )

    state_checkbox = ps.checkbox(
        name="terms-state",
        checked=terms,
        on_change=lambda payload: terms.set(
            payload.get("checked", False) if isinstance(payload, dict) else bool(payload)
        ),
    )

    custom_checkbox = ps.checkbox(
        name="custom",
        checked=custom_checked,
        on_change=handle_custom_change,
        title="Custom change handler",
    )

    checked_checkbox = ps.checkbox(
        name="prechecked",
        checked=True,
    )

    disabled_checkbox = ps.checkbox(
        name="disabled",
        checked=True,
        disabled=True,
        title="Disabled checkbox",
    )

    styled_checkbox = ps.checkbox(
        name="styled",
        checked=False,
        style=pl.style(
            width="1.25rem",
            height="1.25rem",
            cursor="pointer",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage UI Kit — Checkbox",
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                margin_bottom="0.5rem",
            ),
        ),
        pl.text(
            "Interactive checkbox using the existing PyLage engine capability.",
            style=pl.style(margin_bottom="1.5rem"),
        ),

        pl.text("Basic Checkbox", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            basic_checkbox,
            pl.text("Accept terms"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),

        pl.text("pl.State-Bound Checkbox", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            state_checkbox,
            pl.text("Enable terms agreement"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),
        pl.text(terms),

        pl.text("Custom on_change Handler", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            custom_checkbox,
            pl.text("Use custom event handler"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),
        pl.text(status),

        pl.text("Pre-Checked Checkbox", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            checked_checkbox,
            pl.text("Already checked"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),

        pl.text("Disabled Checkbox", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            disabled_checkbox,
            pl.text("Disabled and checked"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),

        pl.text("Styled Checkbox", style=pl.style(font_weight="700", margin_top="1rem")),
        pl.row(
            styled_checkbox,
            pl.text("Custom dimensions and cursor"),
            style=pl.style(align_items="center", gap="0.5rem"),
        ),

        style=pl.style(
            width="100%",
            max_width="700px",
            padding="2rem",
            box_sizing="border-box",
        ),
    )

