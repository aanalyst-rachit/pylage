import pylage as pl
import pylage as ps



def get_app():
    modal_open = pl.state(False)
    action_log = pl.state("No modal action taken yet.")

    def open_modal(e=None):
        modal_open.set(True)
        action_log.set("Modal opened by user.")

    def confirm_action(e=None):
        modal_open.set(False)
        action_log.set("Modal confirmed & closed.")

    def cancel_action(e=None):
        modal_open.set(False)
        action_log.set("Modal cancelled & closed.")

    modal_content = pl.column(
        pl.text("Are you sure you want to deploy the updated PyLage components to production?"),
        pl.row(
            pl.button("Cancel", on_click=cancel_action, variant="secondary"),
            pl.button("Confirm & Deploy", on_click=confirm_action, variant="primary"),
            style=pl.style(
                display="flex",
                justify_content="flex-end",
                gap="0.75rem",
                margin_top="1.5rem",
            ),
        ),
        gap="0.75rem",
    )

    deployment_modal = pl.modal(
        modal_content,
        open=modal_open,
        title="Confirm System Deployment",
        class_name="pylage-ui-kit-modal",
    )

    return pl.column(
        pl.heading("PyLage UI Kit — Modal", level=2),
        pl.text("Reusable Modal recipe composed from the existing UI Kit Dialog and Card components."),
        pl.column(
            pl.text("Modal Status:", style=pl.style(font_weight="bold")),
            pl.text(action_log, style=pl.style(font_weight="bold")),
            gap="0.5rem",
            style=pl.style(
                padding="1rem",
                background_color="#f8fafc",
                border_radius="8px",
            ),
        ),
        pl.button("Open Modal", on_click=open_modal, variant="primary"),
        deployment_modal,
        gap="1.5rem",
        style=pl.style(
            max_width="1200px",
            margin="0 auto",
            padding="2rem",
        ),
    )


if __name__ == "__main__":
    ps.run(
        get_app(),
        title="PyLage Modal Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
