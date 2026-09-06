import pylage as pl


enabled = pl.State(False)
events = pl.State("No event yet")


def handle_change(payload):
    events.set(str(payload))


def get_app():
    return pl.Stack(
        pl.heading("UI Kit Switch — Manual Verification"),

        pl.heading("1. Basic Switch"),
        pl.switch(
            checked=False,
            title="Basic switch",
            class_name="switch-basic",
        ),

        pl.heading("2. Checked Switch"),
        pl.switch(
            checked=True,
            title="Checked switch",
            class_name="switch-checked",
        ),

        pl.heading("3. State-Bound Switch"),
        pl.switch(
            checked=enabled,
            on_change=handle_change,
            title="State-bound switch",
            class_name="switch-state",
        ),
        pl.text("Enabled: "),
        pl.text(enabled),
        pl.text("Last event: "),
        pl.text(events),

        pl.heading("4. Disabled Switch"),
        pl.switch(
            checked=False,
            disabled=True,
            title="Disabled switch",
            class_name="switch-disabled",
        ),

        pl.heading("5. Native Switch Properties"),
        pl.switch(
            checked=True,
            name="notifications",
            id="notifications-switch",
            title="Notification switch",
        ),
    )


if __name__ == "__main__":
    pl.run(get_app())
