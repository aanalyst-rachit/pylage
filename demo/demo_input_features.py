import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps



def get_app():
    name_state = pl.state("Aapka Naam Here")
    submitted_state = pl.state("Form abhi submit nahi hua hai.")

    def handle_name_input(payload):
        if isinstance(payload, dict):
            value = payload.get("value", "")
        else:
            value = "" if payload is None else str(payload)

        name_state.set(value if value else "Aapka Naam Here")

    def handle_submit():
        current = name_state.value
        if isinstance(current, dict):
            current = current.get("value", "")
        submitted_state.set(f"Submitted Name: {current}")

    name_input = pl.input(
        placeholder="Apna naam type karein...",
        on_input=handle_name_input,
        style=pl.style(
            padding="0.75rem 1rem",
            font_size="1rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            width="100%",
            box_sizing="border-box",
            margin_bottom="1rem",
        ),
    )

    email_input = pl.input(
        input_type="email",
        placeholder="Email address",
        name="email",
        required=True,
        style=pl.style(
            padding="0.75rem 1rem",
            font_size="1rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            width="100%",
            box_sizing="border-box",
            margin_bottom="1rem",
        ),
    )

    password_input = pl.input(
        input_type="password",
        placeholder="Password",
        name="password",
        style=pl.style(
            padding="0.75rem 1rem",
            font_size="1rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            width="100%",
            box_sizing="border-box",
            margin_bottom="1rem",
        ),
    )

    disabled_input = pl.input(
        value="Disabled input",
        disabled=True,
        style=pl.style(
            padding="0.75rem 1rem",
            font_size="1rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            width="100%",
            box_sizing="border-box",
            margin_bottom="1rem",
        ),
    )

    submit_button = pl.button(
        "Submit Form",
        on_click=handle_submit,
        style=pl.style(
            padding="0.75rem 1.5rem",
            font_size="1rem",
            font_weight="700",
            border_radius="0.5rem",
            cursor="pointer",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage UI Kit — Input Manual",
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                margin_bottom="0.5rem",
            ),
        ),
        pl.text(
            "Manual verification: text, email, password, disabled and reactive input.",
            style=pl.style(
                margin_bottom="1.5rem",
            ),
        ),

        pl.text("pl.text Input", style=pl.style(font_weight="700")),
        name_input,

        pl.text(
            "Live Preview:",
            style=pl.style(
                font_weight="700",
                margin_top="1rem",
            ),
        ),
        pl.heading(
            name_state,
            style=pl.style(
                font_size="1.25rem",
                margin_bottom="1.5rem",
            ),
        ),

        pl.text("Email Input", style=pl.style(font_weight="700")),
        email_input,

        pl.text("Password Input", style=pl.style(font_weight="700")),
        password_input,

        pl.text("Disabled Input", style=pl.style(font_weight="700")),
        disabled_input,

        submit_button,

        pl.text(
            submitted_state,
            style=pl.style(
                font_weight="600",
                margin_top="1rem",
            ),
        ),

        style=pl.style(
            width="100%",
            max_width="600px",
            min_height="100vh",
            padding="2rem",
            box_sizing="border-box",
        ),
    )


if __name__ == "__main__":
    ps.run(get_app())
