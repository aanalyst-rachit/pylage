import pylage as pl


selected = pl.State("python")
events = pl.State("No event yet")


def handle_change(payload):
    events.set(str(payload))


def get_app():
    return pl.Stack(
        pl.heading("UI Kit Radio — Manual Verification"),

        pl.heading("1. Basic Radio Group"),
        pl.radio_group(
            pl.input(
                input_type="radio",
                name="basic",
                value="one",
                checked=True,
            ),
            pl.input(
                input_type="radio",
                name="basic",
                value="two",
            ),
            pl.input(
                input_type="radio",
                name="basic",
                value="three",
            ),
            title="Basic radio group",
            class_name="radio-basic",
        ),

        pl.heading("2. State-Bound Radio Group"),
        pl.radio_group(
            pl.input(
                input_type="radio",
                name="language",
                value="python",
            ),
            pl.input(
                input_type="radio",
                name="language",
                value="javascript",
            ),
            pl.input(
                input_type="radio",
                name="language",
                value="rust",
            ),
            value=selected,
            on_change=handle_change,
            title="State-bound radio group",
            class_name="radio-state",
        ),
        pl.text("Selected value: "),
        pl.text(selected),
        pl.text("Last event: "),
        pl.text(events),

        pl.heading("3. Disabled Radio Option"),
        pl.radio_group(
            pl.input(
                input_type="radio",
                name="disabled",
                value="available",
            ),
            pl.input(
                input_type="radio",
                name="disabled",
                value="locked",
                disabled=True,
            ),
            title="Disabled option group",
        ),

        pl.heading("4. Native Radio Attributes"),
        pl.radio_group(
            pl.input(
                input_type="radio",
                name="native",
                value="alpha",
                id="radio-alpha",
            ),
            pl.input(
                input_type="radio",
                name="native",
                value="beta",
                id="radio-beta",
            ),
            title="Native radio attributes",
        ),
    )


if __name__ == "__main__":
    pl.run(get_app())
