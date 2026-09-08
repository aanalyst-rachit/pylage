import pylage as pl
import sys
from pathlib import Path

# Project root setup
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pylage as ps


def get_app():
    # pl.State Management
    active_section = pl.state("Section 1")
    expand_count = pl.state(0)

    def select_sec1(e=None):
        active_section.set("Section 1: Engine Architecture")
        expand_count.set(expand_count.value + 1)

    def select_sec2(e=None):
        active_section.set("Section 2: Reactive pl.State Binding")
        expand_count.set(expand_count.value + 1)

    def select_sec3(e=None):
        active_section.set("Section 3: WebSocket Wire Protocol")
        expand_count.set(expand_count.value + 1)

    # Component Composition
    accordion_item_1 = pl.card(
        pl.row(
            pl.heading("1. Engine Architecture", level=4),
            pl.button("Toggle / View", on_click=select_sec1, variant="secondary"),
            style=pl.style(display="flex", justify_content="space-between", align_items="center")
        ),
        pl.text("PyLage compiles pure Python component trees into optimized HTML and client-side reactive bindings."),
        style=pl.style(padding="1rem", margin_bottom="0.5rem", border="1px solid #e2e8f0", border_radius="8px")
    )

    accordion_item_2 = pl.card(
        pl.row(
            pl.heading("2. Reactive pl.State Binding", level=4),
            pl.button("Toggle / View", on_click=select_sec2, variant="secondary"),
            style=pl.style(display="flex", justify_content="space-between", align_items="center")
        ),
        pl.text("pl.state(val) tracks all bound components and triggers minimal microtask-coalesced diff patches."),
        style=pl.style(padding="1rem", margin_bottom="0.5rem", border="1px solid #e2e8f0", border_radius="8px")
    )

    accordion_item_3 = pl.card(
        pl.row(
            pl.heading("3. WebSocket Wire Protocol", level=4),
            pl.button("Toggle / View", on_click=select_sec3, variant="secondary"),
            style=pl.style(display="flex", justify_content="space-between", align_items="center")
        ),
        pl.text("Sub-millisecond binary & JSON UpdateMessages over full-duplex persistent WebSocket connections."),
        style=pl.style(padding="1rem", margin_bottom="0.5rem", border="1px solid #e2e8f0", border_radius="8px")
    )

    accordion_container = pl.accordion(
        accordion_item_1,
        accordion_item_2,
        accordion_item_3,
        class_name="pylage-accordion-group",
        title="PyLage Interactive Accordion Manual Test",
        style=pl.style(width="100%", max_width="700px")
    )

    # Main App Layout
    app = pl.column(
        pl.heading("Accordion Component — Live Manual Test Suite", level=1),
        pl.text("Test collapsible sections, live selection events, and state-bound title rendering."),
        pl.card(
            pl.row(
                pl.text("Currently Active Section: ", style=pl.style(font_weight="bold")),
                pl.heading(active_section, level=3, style=pl.style(color="#2563eb", margin="0")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            pl.row(
                pl.text("Total Toggle Interactions: ", style=pl.style(font_weight="bold")),
                pl.text(expand_count, style=pl.style(color="#10b981", font_weight="bold")),
                style=pl.style(display="flex", align_items="center", gap="0.5rem")
            ),
            style=pl.style(padding="1rem", background="#f8fafc", border_radius="8px", margin_bottom="1.5rem")
        ),
        accordion_container,
        style=pl.style(padding="2rem", gap="1.5rem", font_family="system-ui, sans-serif")
    )

    return app


if __name__ == "__main__":
    app = get_app()
    ps.run(app, title="PyLage Accordion Manual Test", serve=True, host="0.0.0.0", port=3000)
