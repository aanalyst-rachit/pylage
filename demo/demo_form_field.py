from __future__ import annotations

import pylage as pl


def get_app():
    email = pl.state("student@example.com")
    message = pl.state("Hello PyLage")
    country = pl.state("India")

    def update_email(payload):
        if isinstance(payload, dict) and "value" in payload:
            email.set(payload["value"])

    def update_message(payload):
        if isinstance(payload, dict) and "value" in payload:
            message.set(payload["value"])

    def update_country(payload):
        if isinstance(payload, dict) and "value" in payload:
            country.set(payload["value"])

    return pl.stack(
        pl.heading("UI Kit FormField — Manual Verification"),
        pl.text(
            "FormField composition around existing PyLage controls."
        ),

        pl.heading("1. Basic FormField"),
        pl.form_field(
            pl.input(
                value="basic@example.com",
                placeholder="Email address",
            ),
            label="Email",
        ),

        pl.heading("2. Required FormField"),
        pl.form_field(
            pl.input(
                value="",
                placeholder="Required field",
            ),
            label="Full Name",
            required=True,
        ),

        pl.heading("3. Help Text"),
        pl.form_field(
            pl.textarea(
                value="",
                placeholder="Write your message...",
                rows=4,
            ),
            label="Message",
            help_text="Keep your message concise.",
        ),

        pl.heading("4. Error Presentation"),
        pl.form_field(
            pl.input(
                value="invalid-value",
                placeholder="Email address",
            ),
            label="Validated Email",
            required=True,
            error="Please enter a valid email address.",
        ),

        pl.heading("5. State-Bound Input"),
        pl.form_field(
            pl.input(
                value=email,
                placeholder="State-bound email",
                on_input=update_email,
            ),
            label="Reactive Email",
            help_text="Edit this value and watch the State below.",
        ),
        pl.text("Email State:"),
        pl.text(email),

        pl.heading("6. State-Bound Textarea"),
        pl.form_field(
            pl.textarea(
                value=message,
                rows=4,
                on_input=update_message,
            ),
            label="Reactive Message",
            help_text="Textarea is an existing UI Kit control.",
        ),
        pl.text("Message State:"),
        pl.text(message),

        pl.heading("7. State-Bound Select"),
        pl.form_field(
            pl.select(
                pl.option("India", value="India"),
                pl.option("United States", value="United States"),
                pl.option("United Kingdom", value="United Kingdom"),
                pl.option("Canada", value="Canada"),
                value=country,
                on_change=update_country,
            ),
            label="Country",
            help_text="Select control wrapped by FormField.",
        ),
        pl.text("Country State:"),
        pl.text(country),
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage UI Kit FormField Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
