from time import perf_counter

from pylage.ENGINE import Button, Card, Table, Text, Style
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.components.button import button
from pylage.UI.components.card import card
from pylage.UI.components.table import table
from pylage.UI.components.text import text


def _measure(component, iterations=1000):
    start = perf_counter()

    for _ in range(iterations):
        html = render(component)
        assert html

    elapsed = perf_counter() - start

    return {
        "total": elapsed,
        "per_render": elapsed / iterations,
    }


def _build_ui_dashboard():
    return card(
        heading="Dashboard",
        body="System overview",
        footer="Updated now",
        children=(
            button("Refresh"),
            text("Active users", muted=True),
            table(
                data=[["API", "Healthy"], ["DB", "Healthy"]],
                headers=["Service", "Status"],
            ),
        ),
    )


def _build_core_dashboard():
    return Card(
        Button("Refresh"),
        Text("Active users"),
        Table(
            data=[["API", "Healthy"], ["DB", "Healthy"]],
            headers=["Service", "Status"],
        ),
    )


def test_phase16_render_overhead():
    iterations = 1000

    button_style = Style(
        border_radius="var(--radius-lg)",
        font_weight="600",
        cursor="pointer",
        background_color="var(--color-primary)",
        color="var(--color-primary-contrast)",
        border="1px solid var(--color-primary)",
        padding="0.625rem 1rem",
        font_size="1rem",
    )
    text_style = Style()
    card_style = Style(
        background_color="var(--color-background)",
        padding="var(--spacing-lg)",
        border_radius="var(--radius-xl)",
        border="1px solid var(--color-border)",
    )
    table_style = Style(
        width="100%",
        border="1px solid var(--color-border)",
        border_radius="var(--radius-lg)",
        overflow="hidden",
    )

    ui_components = {
        "ui_button": button("Save"),
        "ui_text": text("Hello"),
        "ui_card": card(body="Hello"),
        "ui_table": table(
            data=[["A", "B"], ["C", "D"]],
            headers=["One", "Two"],
        ),
        "ui_dashboard": _build_ui_dashboard(),
    }

    core_components = {
        "core_button": Button("Save", style=button_style),
        "core_text": Text("Hello", style=text_style),
        "core_card": Card(Text("Hello"), style=card_style),
        "core_table": Table(
            data=[["A", "B"], ["C", "D"]],
            headers=["One", "Two"],
            style=table_style,
        ),
        "core_dashboard": _build_core_dashboard(),
    }

    for component in (*ui_components.values(), *core_components.values()):
        assert isinstance(component, Component)

    ui_results = {
        name: _measure(component, iterations)
        for name, component in ui_components.items()
    }
    core_results = {
        name: _measure(component, iterations)
        for name, component in core_components.items()
    }

    print()
    print("===== PHASE 16 — RENDER OVERHEAD =====")
    print(f"iterations        : {iterations}")
    print()

    for name, result in ui_results.items():
        print(name)
        print(f"  total           : {result['total']:.9f}s")
        print(f"  per render      : {result['per_render']:.9f}s")
        print()

    for name, result in core_results.items():
        print(name)
        print(f"  total           : {result['total']:.9f}s")
        print(f"  per render      : {result['per_render']:.9f}s")
        print()

    for result in (*ui_results.values(), *core_results.values()):
        assert result["total"] >= 0
        assert result["per_render"] >= 0
