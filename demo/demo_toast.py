from __future__ import annotations

import pylage as pl


def get_app():
    visible = pl.State(True)

    def toggle_toast(payload=None):
        print("[TOGGLE TOAST] CLICK")
        print("[TOGGLE TOAST] BEFORE:", visible.value)
        visible.set(not visible.value)
        print("[TOGGLE TOAST] AFTER:", visible.value)

    page_style = pl.style(
        width="100%",
        box_sizing="border-box",
        padding="1.5rem",
        gap="1.5rem",
    )

    grid_style = pl.style(
        display="grid",
        grid_template_columns="repeat(2, minmax(0, 1fr))",
        gap="1rem",
        width="100%",
    )

    return pl.column(
        pl.heading("PyLage UI Kit — Toast", level=2),
        pl.text(
            "Semantic feedback toasts using the existing PyLage Toast component."
        ),
        pl.grid(
            pl.toast("Default notification.", variant="default", visible=True),
            pl.toast("Information notification.", variant="info", visible=True),
            pl.toast("Changes saved successfully.", variant="success", visible=True),
            pl.toast("Please review this warning.", variant="warning", visible=True),
            pl.toast("Something went wrong.", variant="danger", visible=True),
            pl.toast("An error occurred.", variant="error", visible=True),
            style=grid_style,
        ),
        pl.card(
            pl.heading("Interactive Toast", level=3),
            pl.text("Toggle the toast visibility using the button below."),
            pl.button("Toggle Toast", on_click=toggle_toast),
            pl.toast(
                "This toast is controlled by pl.State.",
                variant="success",
                visible=visible,
                title="pl.State-driven Toast",
            ),
        ),
        gap="1.5rem",
        style=page_style,
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage Toast Manual",
        serve=True,
        host="127.0.0.1",
        port=8071,
    )
