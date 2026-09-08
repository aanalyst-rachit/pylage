from __future__ import annotations

import pylage as pl


def get_app():
    submitted = pl.state("Form submit nahi hua abhi.")
    submit_count = pl.state(0)

    def handle_submit(payload=None):
        submit_count.set(submit_count.value + 1)

        values = {}
        if isinstance(payload, dict):
            values = payload.get("values", {})

        name = values.get("name", "")
        email = values.get("email", "")
        terms = values.get("terms", "")

        submitted.set(
            f"Name: {name} | Email: {email} | Terms: {terms}"
        )

    page_style = pl.style(
        width="100%",
        max_width="760px",
        margin="0 auto",
        padding="2.5rem 1.5rem",
        box_sizing="border-box",
    )

    card_style = pl.style(
        width="100%",
        padding="2rem",
        gap="1.25rem",
        border="1px solid #e2e8f0",
        border_radius="0.875rem",
        background_color="#ffffff",
        box_shadow="0 8px 30px rgba(15, 23, 42, 0.08)",
        box_sizing="border-box",
    )

    title_style = pl.style(
        font_size="1.75rem",
        font_weight="700",
        margin_bottom="0.25rem",
        color="#0f172a",
    )

    description_style = pl.style(
        font_size="0.95rem",
        line_height="1.5",
        color="#64748b",
        margin_bottom="0.75rem",
    )

    form_style = pl.style(
        width="100%",
        gap="1rem",
    )

    submit_button_style = pl.style(
        width="100%",
        padding="0.7rem 1rem",
        margin_top="0.5rem",
        border_radius="0.5rem",
        font_weight="600",
        cursor="pointer",
    )

    result_style = pl.style(
        width="100%",
        padding="1rem",
        margin_top="0.5rem",
        border="1px solid #dbeafe",
        border_radius="0.625rem",
        background_color="#eff6ff",
        color="#1e3a8a",
        box_sizing="border-box",
    )

    return pl.stack(
        pl.text(
            "Form Component Test Suite",
            style=title_style,
        ),

        pl.text(
            "Testing the public pl.form() API, named controls, "
            "native form submission, FormData payloads, and reactive output.",
            style=description_style,
        ),

        pl.form(
            pl.form_field(
                pl.input(
                    value="Racit",
                    name="name",
                    placeholder="Your name",
                ),
                label="Name",
                required=True,
            ),

            pl.form_field(
                pl.input(
                    value="racit@example.com",
                    name="email",
                    input_type="email",
                    placeholder="Email address",
                ),
                label="Email",
                required=True,
                help_text="Enter a valid email address.",
            ),

            pl.form_field(
                pl.checkbox(
                    checked=False,
                    name="terms",
                ),
                label="Accept terms",
                help_text="This checkbox is submitted with the form.",
            ),

            pl.button(
                "Submit Form",
                type="submit",
                style=submit_button_style,
            ),

            pl.text(
                "Submit count: ",
                style=pl.style(
                    font_weight="600",
                    margin_top="0.75rem",
                ),
            ),

            pl.text(
                submit_count,
                style=pl.style(
                    font_weight="700",
                ),
            ),

            pl.text(
                "Latest submission",
                style=pl.style(
                    font_weight="700",
                    margin_top="0.5rem",
                ),
            ),

            pl.text(
                submitted,
                style=result_style,
            ),

            on_submit=handle_submit,
            method="post",
            action="/submit",
            style=form_style,
        ),

        style=card_style,
    )


if __name__ == "__main__":
    pl.run(
        get_app(),
        title="PyLage Form Manual",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
