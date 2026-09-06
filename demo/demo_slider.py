import pylage as pl


slider_value = pl.State(45)
event_value = pl.State("No event yet")


def handle_slider_input(payload):
    event_value.set(str(payload))


def get_app():
    return pl.Stack(
        pl.heading("UI Kit Slider — Manual Verification"),

        pl.heading("1. Basic Slider"),
        pl.slider(
            value=25,
            min=0,
            max=100,
            step=5,
            title="Basic slider",
        ),

        pl.heading("2. Custom Range"),
        pl.slider(
            value=50,
            min=10,
            max=200,
            step=10,
            title="Custom range slider",
        ),

        pl.heading("3. State-Bound Slider"),
        pl.slider(
            value=slider_value,
            min=0,
            max=100,
            step=5,
            title="State-bound slider",
            on_input=handle_slider_input,
        ),
        pl.text("Slider value: "),
        pl.text(slider_value),
        pl.text("Last input event: "),
        pl.text(event_value),

        pl.heading("4. Disabled Slider"),
        pl.slider(
            value=40,
            min=0,
            max=100,
            step=1,
            disabled=True,
            title="Disabled slider",
        ),

        pl.heading("5. Native Slider Properties"),
        pl.slider(
            value=75,
            min=0,
            max=100,
            step=5,
            name="volume",
            id="volume-slider",
            title="Volume slider",
        ),
    )


if __name__ == "__main__":
    pl.run(get_app())
