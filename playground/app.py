
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

    header = pl.column(
        pl.row(
            pl.row(
                pl.text(
                    'Py',
                    style=pl.style(
                        width='2.8rem',
                        height='2.8rem',
                        display='flex',
                        align_items='center',
                        justify_content='center',
                        background_color='#60a5fa',
                        color='#0f172a',
                        border_radius='50%',
                        font_size='1.15rem',
                        font_weight='800',
                    ),
                ),
                pl.column(
                    pl.text(
                        'PyLage',
                        style=pl.style(
                            color='#f8fafc',
                            font_size='2rem',
                            font_weight='800',
                            letter_spacing='-0.035em',
                            line_height='1',
                        ),
                    ),
                    pl.text(
                        'Server-Driven Reactive UI Framework for Python',
                        style=pl.style(
                            color='#94a3b8',
                            font_size='0.82rem',
                            margin_top='0.35rem',
                        ),
                    ),
                    style=pl.style(
                        gap='0.1rem',
                        margin_left='0.7rem',
                    ),
                ),
                style=pl.style(
                    align_items='center',
                ),
            ),
            pl.row(
                pl.text(
                    'Docs',
                    id='pylage-playground-docs',
                    style=pl.style(
                        color='#cbd5e1',
                        font_size='0.78rem',
                        font_weight='600',
                        cursor='pointer',
                    ),
                ),
                pl.text(
                    'Install',
                    id='pylage-playground-install',
                    style=pl.style(
                        color='#cbd5e1',
                        font_size='0.78rem',
                        font_weight='600',
                        cursor='pointer',
                    ),
                ),
                pl.text(
                    'GitHub',
                    id='pylage-playground-github',
                    style=pl.style(
                        color='#cbd5e1',
                        font_size='0.78rem',
                        font_weight='600',
                        cursor='pointer',
                    ),
                ),
                style=pl.style(
                    gap='1.1rem',
                    align_items='center',
                ),
            ),
            style=pl.style(
                width='100%',
                justify_content='space-between',
                align_items='center',
                padding='0 0 1.25rem',
                border_bottom='1px solid #334155',
            ),
        ),
        pl.text(
            'Build web interfaces in pure Python — no HTML, no JavaScript.',
            style=pl.style(
                color='#6ee7b7',
                font_size='1.18rem',
                font_weight='800',
                line_height='1.4',
                margin_top='1rem',
            ),
        ),
        pl.row(
            pl.text('State', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            pl.text('→', style=pl.style(color='#94a3b8', font_size='0.9rem')),
            pl.text('DependencyGraph', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            pl.text('→', style=pl.style(color='#94a3b8', font_size='0.9rem')),
            pl.text('DirtyNodes', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            pl.text('→', style=pl.style(color='#94a3b8', font_size='0.9rem')),
            pl.text('Scheduler', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            pl.text('→', style=pl.style(color='#94a3b8', font_size='0.9rem')),
            pl.text('Diff', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            pl.text('→', style=pl.style(color='#94a3b8', font_size='0.9rem')),
            pl.text('Patch', style=pl.style(
                color='#f8fafc',
                background_color='#172033',
                border='1px solid #60a5fa',
                border_radius='0.35rem',
                padding='0.3rem 0.55rem',
                font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                font_size='0.72rem',
            )),
            style=pl.style(
                width='100%',
                align_items='center',
                flex_wrap='wrap',
                gap='0.45rem',
                margin_top='1.15rem',
            ),
        ),
        pl.row(
            pl.card(
                pl.text('~3.5μs', style=pl.style(
                    color='#6ee7b7',
                    font_size='1.25rem',
                    font_weight='800',
                    text_align='center',
                )),
                pl.text('State update', style=pl.style(
                    color='#94a3b8',
                    font_size='0.68rem',
                    text_align='center',
                    margin_top='0.35rem',
                )),
                style=pl.style(
                    background_color='#172033',
                    border='0',
                    border_radius='0.55rem',
                    padding='1rem',
                    width='100%',
                    box_sizing='border-box',
                ),
            ),
            pl.card(
                pl.text('~4.6μs', style=pl.style(
                    color='#6ee7b7',
                    font_size='1.25rem',
                    font_weight='800',
                    text_align='center',
                )),
                pl.text('Diff compute', style=pl.style(
                    color='#94a3b8',
                    font_size='0.68rem',
                    text_align='center',
                    margin_top='0.35rem',
                )),
                style=pl.style(
                    background_color='#172033',
                    border='0',
                    border_radius='0.55rem',
                    padding='1rem',
                    width='100%',
                    box_sizing='border-box',
                ),
            ),
            pl.card(
                pl.text('~6.8μs', style=pl.style(
                    color='#6ee7b7',
                    font_size='1.25rem',
                    font_weight='800',
                    text_align='center',
                )),
                pl.text('Patch convert', style=pl.style(
                    color='#94a3b8',
                    font_size='0.68rem',
                    text_align='center',
                    margin_top='0.35rem',
                )),
                style=pl.style(
                    background_color='#172033',
                    border='0',
                    border_radius='0.55rem',
                    padding='1rem',
                    width='100%',
                    box_sizing='border-box',
                ),
            ),
            pl.card(
                pl.text('~29μs', style=pl.style(
                    color='#6ee7b7',
                    font_size='1.25rem',
                    font_weight='800',
                    text_align='center',
                )),
                pl.text('Schedule flush', style=pl.style(
                    color='#94a3b8',
                    font_size='0.68rem',
                    text_align='center',
                    margin_top='0.35rem',
                )),
                style=pl.style(
                    background_color='#172033',
                    border='0',
                    border_radius='0.55rem',
                    padding='1rem',
                    width='100%',
                    box_sizing='border-box',
                ),
            ),
            style=pl.style(
                width='100%',
                display='grid',
                grid_template_columns='repeat(4, minmax(0, 1fr))',
                gap='0.7rem',
                margin_top='1.15rem',
            ),
        ),
        pl.row(
            pl.text('•  Pure Python UI', style=pl.style(color='#cbd5e1', font_size='0.73rem')),
            pl.text('•  WebSocket real-time sync', style=pl.style(color='#cbd5e1', font_size='0.73rem')),
            pl.text('•  id-based DOM diffing', style=pl.style(color='#cbd5e1', font_size='0.73rem')),
            pl.text('•  1,000+ automated tests', style=pl.style(color='#cbd5e1', font_size='0.73rem')),
            style=pl.style(
                width='100%',
                flex_wrap='wrap',
                gap='1.2rem',
                margin_top='1rem',
            ),
        ),
        pl.row(
            pl.text(
                'pip install pylage',
                style=pl.style(
                    color='#60a5fa',
                    font_family='ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace',
                    font_size='0.76rem',
                    font_weight='600',
                ),
            ),
            pl.text(
                'github.com/aanalyst-rachit/pylage',
                style=pl.style(
                    color='#64748b',
                    font_size='0.72rem',
                ),
            ),
            style=pl.style(
                width='100%',
                justify_content='space-between',
                align_items='center',
                padding='1rem 0 0',
                margin_top='0.9rem',
                border_top='1px solid #334155',
            ),
        ),
        style=pl.style(
            width='100%',
            padding='1.25rem 1.25rem 1.15rem',
            background_color='#0f172a',
            color='#f8fafc',
            border='1px solid #1e293b',
            border_top='3px solid #60a5fa',
            border_radius='1rem',
            box_shadow='0 18px 45px rgba(15, 23, 42, 0.18)',
            box_sizing='border-box',
            gap='0.15rem',
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
            playground_intro,
            playground_panel,
            features,
            workflow,
            footer,
            style=container_style,
        ),
        style=page_style,
    )