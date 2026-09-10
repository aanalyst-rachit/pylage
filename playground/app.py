
from __future__ import annotations

import pylage as pl


def get_app():
    page_style = pl.style(
        width="100%",
        min_height="100vh",
        background_color="#f8fafc",
        color="#0f172a",
        font_family=(
            "Inter, ui-sans-serif, system-ui, -apple-system, "
            "BlinkMacSystemFont, Segoe UI, sans-serif"
        ),
    )

    container_style = pl.style(
        width="100%",
        max_width="1180px",
        margin="1rem auto",
        padding="1.5rem",
        box_sizing="border-box",
    )

    muted_style = pl.style(
        color="#64748b",
        font_size="0.9rem",
        line_height="1.6",
    )

    eyebrow_style = pl.style(
        color="#2563eb",
        font_size="0.75rem",
        font_weight="700",
        letter_spacing="0.12em",
        text_transform="uppercase",
    )

    section_title_style = pl.style(
        color="#0f172a",
        font_size="1.35rem",
        font_weight="700",
        margin="0",
    )

    header = pl.row(
        pl.column(
            pl.text(
                "PyLage",
                style=pl.style(
                    color="#0f172a",
                    font_size="1.35rem",
                    font_weight="800",
                    letter_spacing="-0.03em",
                ),
            ),
            pl.text(
                "Python-native UI for the web",
                style=pl.style(
                    color="#64748b",
                    font_size="0.78rem",
                    margin_top="0.15rem",
                ),
            ),
            style=pl.style(
                gap="0.1rem",
            ),
        ),
        pl.row(
            pl.text(
                "Docs",
                style=pl.style(
                    color="#475569",
                    font_size="0.82rem",
                    font_weight="600",
                    cursor="pointer",
                ),
            ),
            pl.text(
                "GitHub",
                style=pl.style(
                    color="#475569",
                    font_size="0.82rem",
                    font_weight="600",
                    cursor="pointer",
                ),
            ),
            style=pl.style(
                gap="1.25rem",
                align_items="center",
            ),
        ),
        style=pl.style(
            width="100%",
            justify_content="space-between",
            align_items="center",
            padding="0.35rem 0 1.5rem",
        ),
    )

    visual_block = pl.column(
        pl.image(
            src="/data/PyLage_Portfolio_Cover.png",
            alt="PyLage visual",
            width="100%",
            height="430px",
            style=pl.style(
                width="100%",
                height="430px",
                border_radius="1.25rem",
                object_fit="cover",
                object_position="center",
                display="block",
            ),
        ),
        style=pl.style(
            width="100%",
            border_radius="1.25rem",
            overflow="hidden",
            box_shadow="0 18px 45px rgba(15, 23, 42, 0.16)",
        ),
    )

    playground_intro = pl.column(
        pl.text(
            "PYLAGE PLAYGROUND",
            style=eyebrow_style,
        ),
        pl.text(
            "Build the interface in Python.",
            style=pl.style(
                color="#0f172a",
                font_size="2rem",
                font_weight="800",
                line_height="1.15",
                margin_top="0.6rem",
                max_width="720px",
            ),
        ),
        pl.text(
            "Write PyLage code, run it, and see the resulting UI directly in the browser.",
            style=pl.style(
                color="#64748b",
                font_size="1rem",
                line_height="1.7",
                margin_top="0.6rem",
                max_width="680px",
            ),
        ),
        style=pl.style(
            width="100%",
            gap="0.1rem",
            margin_top="2rem",
            margin_bottom="1rem",
        ),
    )

    editor_code = pl.state(
        """import pylage as pl

name = pl.state("PyLage")

pl.card(
    pl.text(
        "Hello from " + name.value,
        style=pl.style(
            font_size="1.5rem",
            font_weight="700",
            color="#0f172a",
        ),
    ),
    pl.text(
        "This UI was created directly from Python.",
        style=pl.style(
            color="#64748b",
            margin_top="0.5rem",
        ),
    ),
    style=pl.style(
        padding="1.5rem",
        border="1px solid #e2e8f0",
        border_radius="0.9rem",
        background_color="#ffffff",
    ),
)
"""
    )

    editor_header = pl.row(
        pl.column(
            pl.text(
                "Python",
                style=pl.style(
                    color="#334155",
                    font_weight="700",
                    font_size="0.85rem",
                ),
            ),
            pl.text(
                "Live editor",
                style=pl.style(
                    color="#94a3b8",
                    font_size="0.72rem",
                    margin_top="0.15rem",
                ),
            ),
            style=pl.style(
                gap="0.1rem",
            ),
        ),
        pl.text(
            "PyLage",
            style=pl.style(
                color="#64748b",
                font_size="0.75rem",
            ),
        ),
        style=pl.style(
            width="100%",
            justify_content="space-between",
            align_items="center",
            margin_bottom="0.75rem",
        ),
    )

    editor = pl.textarea(
        editor_code,
        id="pylage-playground-editor",
        style=pl.style(
            width="100%",
            min_height="330px",
            background_color="#0f172a",
            color="#f8fafc",
            font_family=(
                "ui-monospace, SFMono-Regular, Menlo, Monaco, "
                "Consolas, monospace"
            ),
            font_size="0.84rem",
            line_height="1.6",
            border_radius="0.75rem",
            padding="1rem",
            border="1px solid #1e293b",
            box_sizing="border-box",
        ),
    )

    run_button = pl.button(
        "Run",
        id="pylage-playground-run",
        style=pl.style(
            background_color="#0f172a",
            color="#ffffff",
            border="1px solid #1e293b",
            border_radius="0.7rem",
            padding="0.7rem 1rem",
            font_weight="700",
            cursor="pointer",
            margin_top="0.8rem",
        ),
    )

    editor_panel = pl.column(
        editor_header,
        editor,
        run_button,
        style=pl.style(
            width="100%",
            padding="1.25rem",
            box_sizing="border-box",
        ),
    )

    preview_header = pl.row(
        pl.column(
            pl.text(
                "Preview",
                style=pl.style(
                    color="#334155",
                    font_weight="700",
                    font_size="0.85rem",
                ),
            ),
            pl.text(
                "Rendered UI",
                style=pl.style(
                    color="#94a3b8",
                    font_size="0.72rem",
                    margin_top="0.15rem",
                ),
            ),
            style=pl.style(
                gap="0.1rem",
            ),
        ),
        style=pl.style(
            width="100%",
            justify_content="space-between",
            align_items="center",
            margin_bottom="0.75rem",
        ),
    )

    status = pl.text(
        "Ready",
        id="pylage-playground-status",
        style=pl.style(
            color="#64748b",
            font_size="0.75rem",
            margin_top="0.65rem",
        ),
    )

    preview_area = pl.column(
        id="pylage-playground-preview",
        style=pl.style(
            width="100%",
            min_height="390px",
            background_color="#f8fafc",
            border="1px solid #e2e8f0",
            border_radius="0.75rem",
            padding="1rem",
            box_sizing="border-box",
            overflow="auto",
        ),
    )

    preview = pl.card(
        pl.heading(
            "Live Preview",
            level=3,
            style=pl.style(
                color="#0f172a",
                font_size="1rem",
                font_weight="700",
                margin="0 0 0.75rem",
            ),
        ),
        preview_area,
        style=pl.style(
            width="100%",
            padding="1rem",
            border="1px solid #e2e8f0",
            border_radius="0.75rem",
            background_color="#ffffff",
            box_sizing="border-box",
        ),
    )

    def run_preview():
        preview.set_children(
            pl.heading(
                "Live Preview",
                level=3,
                style=pl.style(
                    color="#0f172a",
                    font_size="1rem",
                    font_weight="700",
                    margin="0 0 0.75rem",
                ),
            ),
            pl.text("Preview updated from the editor."),
            preview_area,
        )

    run_button.events["click"] = run_preview

    preview_panel = pl.column(
        preview_header,
        preview,
        status,
        style=pl.style(
            width="100%",
            padding="1.25rem",
            box_sizing="border-box",
        ),
    )

    playground_panel = pl.row(
        editor_panel,
        preview_panel,
        style=pl.style(
            width="100%",
            display="grid",
            grid_template_columns="minmax(0, 1fr) minmax(0, 1fr)",
            gap="1px",
            background_color="#e2e8f0",
            border="1px solid #e2e8f0",
            border_radius="1rem",
            overflow="hidden",
            box_shadow="0 12px 30px rgba(15, 23, 42, 0.06)",
        ),
    )

    feature_card = pl.column(
        pl.text(
            "Python first",
            style=pl.style(
                color="#0f172a",
                font_weight="700",
                font_size="0.95rem",
            ),
        ),
        pl.text(
            "Build interfaces using familiar Python APIs instead of switching between multiple UI layers.",
            style=muted_style,
        ),
        style=pl.style(
            padding="1.25rem",
            gap="0.45rem",
        ),
    )

    reactive_card = pl.column(
        pl.text(
            "Reactive by design",
            style=pl.style(
                color="#0f172a",
                font_weight="700",
                font_size="0.95rem",
            ),
        ),
        pl.text(
            "Use PyLage State and existing component mutation APIs to create interactive experiences.",
            style=muted_style,
        ),
        style=pl.style(
            padding="1.25rem",
            gap="0.45rem",
        ),
    )

    browser_card = pl.column(
        pl.text(
            "Runs in the browser",
            style=pl.style(
                color="#0f172a",
                font_weight="700",
                font_size="0.95rem",
            ),
        ),
        pl.text(
            "The playground executes Python through the browser runtime and renders the resulting PyLage component.",
            style=muted_style,
        ),
        style=pl.style(
            padding="1.25rem",
            gap="0.45rem",
        ),
    )

    features = pl.row(
        feature_card,
        reactive_card,
        browser_card,
        style=pl.style(
            width="100%",
            display="grid",
            grid_template_columns="repeat(3, minmax(0, 1fr))",
            gap="1rem",
            margin_top="1.5rem",
        ),
    )

    workflow = pl.card(
        pl.column(
            pl.text(
                "One simple workflow",
                style=section_title_style,
            ),
            pl.text(
                "Write Python → run it → inspect the rendered component → iterate.",
                style=muted_style,
            ),
            pl.row(
                pl.text(
                    "01  Write",
                    style=pl.style(
                        color="#2563eb",
                        font_weight="700",
                        font_size="0.82rem",
                    ),
                ),
                pl.text(
                    "02  Run",
                    style=pl.style(
                        color="#2563eb",
                        font_weight="700",
                        font_size="0.82rem",
                    ),
                ),
                pl.text(
                    "03  See",
                    style=pl.style(
                        color="#2563eb",
                        font_weight="700",
                        font_size="0.82rem",
                    ),
                ),
                pl.text(
                    "04  Iterate",
                    style=pl.style(
                        color="#2563eb",
                        font_weight="700",
                        font_size="0.82rem",
                    ),
                ),
                style=pl.style(
                    width="100%",
                    flex_wrap="wrap",
                    gap="1.5rem",
                    margin_top="1.25rem",
                ),
            ),
            style=pl.style(
                gap="0.45rem",
            ),
        ),
        style=pl.style(
            width="100%",
            padding="1.5rem",
            margin_top="1.5rem",
            box_sizing="border-box",
        ),
    )

    footer = pl.row(
        pl.text(
            "PyLage",
            style=pl.style(
                color="#0f172a",
                font_weight="700",
                font_size="0.82rem",
            ),
        ),
        pl.text(
            "Python-native UI, from component to browser.",
            style=pl.style(
                color="#94a3b8",
                font_size="0.75rem",
            ),
        ),
        style=pl.style(
            width="100%",
            justify_content="space-between",
            align_items="center",
            padding="1.5rem 0 0.5rem",
        ),
    )

    return pl.column(
        pl.column(
            header,
            visual_block,
            playground_intro,
            playground_panel,
            features,
            workflow,
            footer,
            style=container_style,
        ),
        style=page_style,
    )