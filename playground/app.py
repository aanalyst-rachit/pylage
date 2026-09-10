import pylage as pl


def get_app() -> pl.column:
    header = pl.column(
        pl.row(
            pl.heading("PyLage", level=3),
            pl.row(
                pl.text("Features"),
                pl.text("Documentation"),
                pl.text("GitHub"),
                style=pl.style(
                    display="flex",
                    gap="1rem",
                    align_items="center",
                ),
            ),
            style=pl.style(
                display="flex",
                align_items="center",
                justify_content="space-between",
                padding="1rem 0",
                width="100%",
            ),
        ),
        pl.divider(),
    )

    hero = pl.hero(
        title="Build Python UIs. Live.",
        description="Simple, ultrafast, low-latency Python UI for building reactive applications without a frontend build system.",
        actions=[
            pl.button("Open Playground"),
            pl.button("Read Documentation"),
        ],
        style=pl.style(
            width="100%",
            padding="5rem 2rem",
            background="#f8fafc",
            border="1px solid #e2e8f0",
            border_radius="1rem",
            box_sizing="border-box",
            align_items="center",
        ),
    )

    editor_code = pl.state("""import pylage as pl

pl.column(
    pl.heading("Hello, PyLage", level=2),
    pl.text("Edit this example and press Run."),
    pl.button("Get Started"),
)""")

    preview_area = pl.card(
        pl.heading("Live Preview", level=3),
        pl.text("Press Run to update the preview.", style=pl.style(color="#64748b")),
        pl.column(
            pl.heading("Hello, PyLage", level=2),
            pl.text("Your PyLage preview will appear here."),
            pl.button("Get Started"),
            style=pl.style(width="100%", gap="0.75rem"),
        ),
        id="pylage-playground-preview",
        style=pl.style(
            width="50%",
            min_height="360px",
            padding="1.25rem",
            background="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="0.75rem",
            box_sizing="border-box",
        ),
    )

    def run_preview(_event=None):
        preview_area.set_children(
            pl.heading("Live Preview", level=3),
            pl.text("Preview updated from the editor.", style=pl.style(color="#64748b")),
            pl.card(
                pl.text("Python code received", style=pl.style(font_weight="600")),
                pl.text(
                    editor_code.value,
                    style=pl.style(
                        white_space="pre-wrap",
                        font_family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace",
                    ),
                ),
                style=pl.style(
                    width="100%",
                    padding="1rem",
                    background="#f8fafc",
                    border="1px solid #e2e8f0",
                    border_radius="0.75rem",
                    box_sizing="border-box",
                ),
            ),
        )

        pl.text("Ready", id="pylage-playground-status", style=pl.style(color="#64748b")),

    playground_panel = pl.card(
        pl.heading("Python → UI", level=3),
        pl.text(
            "Write Python on the left, press Run, and inspect the live preview on the right.",
            style=pl.style(color="#64748b"),
        ),
        pl.row(
            pl.column(
                pl.text("Python", style=pl.style(font_weight="600")),
                pl.textarea(editor_code, id="pylage-playground-editor"),
                pl.button("Run", id="pylage-playground-run", on_click=run_preview),
                style=pl.style(width="50%", gap="0.75rem"),
            ),
            preview_area,
            style=pl.style(
                width="100%",
                align_items="stretch",
                gap="1rem",
            ),
        ),
        style=pl.style(
            width="100%",
            padding="1.5rem",
            background="#ffffff",
            border="1px solid #e2e8f0",
            border_radius="1rem",
            box_sizing="border-box",
        ),
    )

    features = pl.feature_section(
        title="Why PyLage?",
        description="Everything you need for fast Python-first UI development.",
        features=[
            {"title": "Python-first", "description": "Build your UI directly with Python instead of maintaining a separate frontend stack."},
            {"title": "Reactive", "description": "State-driven interfaces update through PyLage’s reactive runtime."},
            {"title": "Low latency", "description": "Differential updates keep interactions fast and lightweight."},
            {"title": "No build system", "description": "Focus on your application without a JavaScript frontend build pipeline."},
        ],
        style=pl.style(width="100%", gap="1.5rem"),
    )

    workflow = pl.section(
        pl.heading("From Python to UI", level=2),
        pl.text("The playground workflow: write Python on the left, run it, and inspect the resulting PyLage UI on the right."),
        pl.row(
            pl.card(pl.heading("1. Write", level=3), pl.text("Python code")),
            pl.card(pl.heading("2. Run", level=3), pl.text("Execute the example")),
            pl.card(pl.heading("3. See", level=3), pl.text("Live UI preview")),
            style=pl.style(width="100%", gap="1rem"),
        ),
        style=pl.style(width="100%", padding="2rem 0"),
    )

    cta = pl.cta(
        title="Ready to build with PyLage?",
        description="Start with the playground, then explore the full documentation and framework APIs.",
        actions=[
            pl.button("Start Building"),
            pl.button("Explore Docs"),
        ],
        style=pl.style(
            width="100%",
            padding="3rem 2rem",
            background="#f8fafc",
            border="1px solid #e2e8f0",
            border_radius="1rem",
            box_sizing="border-box",
        ),
    )

    footer = pl.row(
        pl.text("PyLage — Simple, Ultrafast, Low-Latency Python UI"),
        pl.text("Documentation · GitHub"),
        style=pl.style(
            width="100%",
            padding="1.5rem 0",
            justify_content="space-between",
            color="#64748b",
        ),
    )

    return pl.column(
        header,
        hero,
        playground_panel,
        features,
        workflow,
        cta,
        footer,
        style=pl.style(
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding="0 1.5rem 3rem",
            gap="2rem",
            box_sizing="border-box",
        ),
    )


if __name__ == "__main__":
    pl.run(get_app(), title="PyLage Playground", serve=True, port=8000, host="0.0.0.0", open_browser=True)
