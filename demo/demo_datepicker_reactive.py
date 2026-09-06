import pylage as pl


selected_date = pl.State("2026-09-03")
last_event = pl.State("No input event yet")


def handle_date_input(payload):
    last_event.set(str(payload))


def set_today():
    selected_date.set("2026-09-03")


def set_next_week():
    selected_date.set("2026-09-10")


def get_app():
    return pl.Stack(
        pl.heading("UI Kit DatePicker — Manual Verification"),

        pl.heading("1. Basic DatePicker"),
        pl.datepicker(
            value="2026-09-03",
            title="Basic date picker",
        ),

        pl.heading("2. State-Bound DatePicker"),
        pl.datepicker(
            value=selected_date,
            min="2026-01-01",
            max="2026-12-31",
            title="State-bound date picker",
            on_input=handle_date_input,
        ),
        pl.text("Selected date: "),
        pl.text(selected_date),
        pl.text("Last input event: "),
        pl.text(last_event),

        pl.heading("3. Programmatic State Update"),
        pl.text("Use these buttons to update the DatePicker through State:"),
        pl.button("Today", on_click=set_today),
        pl.button("+1 Week", on_click=set_next_week),

        pl.heading("4. Disabled DatePicker"),
        pl.datepicker(
            value="2026-09-03",
            disabled=True,
            title="Disabled date picker",
        ),

        pl.heading("5. Native DatePicker Properties"),
        pl.datepicker(
            value="2026-09-15",
            min="2026-09-01",
            max="2026-09-30",
            name="appointment_date",
            id="appointment-date",
            title="September appointment date",
        ),
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage UI Kit DatePicker Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
