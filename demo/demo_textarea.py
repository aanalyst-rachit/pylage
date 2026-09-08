import pylage as pl
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps



def get_app():
    # Reactive state used to verify real browser input binding.
    message = pl.state("")
    input_count = pl.state(0)
    custom_value = pl.state("")

    def handle_custom_input(payload=None):
        if isinstance(payload, dict) and "value" in payload:
            custom_value.set(payload["value"])

    basic = pl.textarea(
        "",
        placeholder="Type something here...",
        rows=5,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    state_bound = pl.textarea(
        message,
        placeholder="Type to update the reactive state...",
        rows=5,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #2563eb",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    custom_handler = pl.textarea(
        "",
        placeholder="Custom on_input handler...",
        rows=4,
        on_input=handle_custom_input,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #7c3aed",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    disabled = pl.textarea(
        "This textarea is disabled.",
        rows=3,
        disabled=True,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            background_color="#f1f5f9",
            box_sizing="border-box",
        ),
    )

    configured = pl.textarea(
        "Textarea with configured attributes.",
        placeholder="Configured placeholder",
        name="manual-notes",
        rows=4,
        cols=40,
        required=True,
        minlength=3,
        maxlength=500,
        style=pl.style(
            width="100%",
            padding="0.75rem",
            border="1px solid #94a3b8",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

    return pl.column(
        pl.heading(
            "PyLage Textarea — Live Manual",
            level=1,
            style=pl.style(
                font_size="1.75rem",
                font_weight="700",
                margin_bottom="0.5rem",
            ),
        ),
        pl.text(
            "Manual verification of textarea rendering, attributes, disabled state, "
            "pl.State binding, and custom input handling.",
            style=pl.style(
                color="#64748b",
                margin_bottom="1.5rem",
            ),
        ),

        pl.card(
            pl.heading("1. Basic Textarea", level=3),
            pl.text(
                "Verify that the textarea renders as a native multi-line input "
                "with placeholder and configurable rows.",
                style=pl.style(color="#64748b", margin_bottom="0.75rem"),
            ),
            basic,
            style=pl.style(
                padding="1.25rem",
                margin_bottom="1rem",
                border="1px solid #e2e8f0",
                border_radius="0.75rem",
            ),
        ),

        pl.card(
            pl.heading("2. pl.State-Bound Textarea", level=3),
            pl.text(
                "Type into the textarea and verify that the reactive state below updates.",
                style=pl.style(color="#64748b", margin_bottom="0.75rem"),
            ),
            state_bound,
            pl.row(
                pl.text(
                    "Reactive value: ",
                    style=pl.style(font_weight="700"),
                ),
                pl.text(
                    message,
                    style=pl.style(
                        color="#2563eb",
                        font_weight="700",
                        white_space="pre-wrap",
                    ),
                ),
                style=pl.style(
                    display="flex",
                    align_items="flex-start",
                    gap="0.5rem",
                    margin_top="0.75rem",
                ),
            ),
            style=pl.style(
                padding="1.25rem",
                margin_bottom="1rem",
                border="1px solid #bfdbfe",
                border_radius="0.75rem",
                background_color="#eff6ff",
            ),
        ),

        pl.card(
            pl.heading("3. Custom Input Handler", level=3),
            pl.text(
                "Verify that an explicitly supplied on_input handler is preserved.",
                style=pl.style(color="#64748b", margin_bottom="0.75rem"),
            ),
            custom_handler,
            pl.row(
                pl.text(
                    "Custom handler value: ",
                    style=pl.style(font_weight="700"),
                ),
                pl.text(
                    custom_value,
                    style=pl.style(
                        color="#7c3aed",
                        font_weight="700",
                        white_space="pre-wrap",
                    ),
                ),
                style=pl.style(
                    display="flex",
                    align_items="flex-start",
                    gap="0.5rem",
                    margin_top="0.75rem",
                ),
            ),
            style=pl.style(
                padding="1.25rem",
                margin_bottom="1rem",
                border="1px solid #ddd6fe",
                border_radius="0.75rem",
                background_color="#f5f3ff",
            ),
        ),

        pl.card(
            pl.heading("4. Disabled Textarea", level=3),
            pl.text(
                "Verify that disabled=True prevents editing.",
                style=pl.style(color="#64748b", margin_bottom="0.75rem"),
            ),
            disabled,
            style=pl.style(
                padding="1.25rem",
                margin_bottom="1rem",
                border="1px solid #e2e8f0",
                border_radius="0.75rem",
            ),
        ),

        pl.card(
            pl.heading("5. Native Textarea Attributes", level=3),
            pl.text(
                "Verify name, rows, cols, required, minlength, maxlength, "
                "and placeholder attributes.",
                style=pl.style(color="#64748b", margin_bottom="0.75rem"),
            ),
            configured,
            style=pl.style(
                padding="1.25rem",
                margin_bottom="1rem",
                border="1px solid #e2e8f0",
                border_radius="0.75rem",
            ),
        ),

        style=pl.style(
            width="100%",
            max_width="800px",
            min_height="100vh",
            padding="2rem",
            margin="0 auto",
            background_color="#f8fafc",
            box_sizing="border-box",
            font_family="system-ui, sans-serif",
        ),
    )


if __name__ == "__main__":
    app = get_app()
    ps.run(
        app,
        title="PyLage Textarea Manual Test",
        serve=True,
        host="0.0.0.0",
        port=3000,
    )
