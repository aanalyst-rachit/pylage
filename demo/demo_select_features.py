import pylage as pl
import pylage as ps


def get_app():
    selected_language = pl.state("python")
    selected_country = pl.state("india")
    custom_status = pl.state("Custom handler not triggered yet.")

    def handle_country_change(payload):
        if isinstance(payload, dict):
            value = payload.get("value", "")
        else:
            value = str(payload)

        custom_status.set(f"Selected country: {value}")

    basic_select = ps.select(
        pl.option("Python", value="python"),
        pl.option("JavaScript", value="javascript"),
        pl.option("Rust", value="rust"),
        value="python",
        name="language",
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    state_select = ps.select(
        pl.option("Python", value="python"),
        pl.option("JavaScript", value="javascript"),
        pl.option("Rust", value="rust"),
        value=selected_language,
        name="state-language",
        on_change=lambda payload: selected_language.set(
            payload.get("value", "") if isinstance(payload, dict) else str(payload)
        ),
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    custom_select = ps.select(
        pl.option("India", value="india"),
        pl.option("Japan", value="japan"),
        pl.option("Nepal", value="nepal"),
        value=selected_country,
        name="country",
        on_change=handle_country_change,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    disabled_select = ps.select(
        pl.option("Locked option", value="locked"),
        value="locked",
        disabled=True,
        name="disabled-select",
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    multiple_select = ps.select(
        pl.option("Python", value="python"),
        pl.option("JavaScript", value="javascript"),
        pl.option("Rust", value="rust"),
        pl.option("Go", value="go"),
        multiple=True,
        size=4,
        name="multiple-languages",
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage UI Kit — Select",
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                margin_bottom="0.5rem",
            ),
        ),

        pl.text(
            "Basic Select",
            style=pl.style(font_weight="700", margin_top="1rem"),
        ),
        basic_select,

        pl.text(
            "pl.State-Bound Select",
            style=pl.style(font_weight="700", margin_top="1rem"),
        ),
        state_select,
        pl.text(selected_language),

        pl.text(
            "Custom on_change Handler",
            style=pl.style(font_weight="700", margin_top="1rem"),
        ),
        custom_select,
        pl.text(custom_status),

        pl.text(
            "Disabled Select",
            style=pl.style(font_weight="700", margin_top="1rem"),
        ),
        disabled_select,

        pl.text(
            "Multiple Select",
            style=pl.style(font_weight="700", margin_top="1rem"),
        ),
        multiple_select,

        style=pl.style(
            width="100%",
            max_width="700px",
            padding="2rem",
            box_sizing="border-box",
        ),
    )
