from time import perf_counter

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.UI.components.button import button
from pylage.UI.components.card import card
from pylage.ENGINE import Column
from pylage.UI.components.dashboard_section import dashboard_section
from pylage.UI.components.metric import metric
from pylage.UI.components.table import table
from pylage.UI.components.text import text


def _build_large_dashboard(card_count=100):
    cards = []

    for index in range(card_count):
        cards.append(
            card(
                metric(
                    label=f"Metric {index}",
                    value=str(index * 100),
                    delta=f"+{index}%",
                ),
                text(f"Status for metric {index}"),
                button("View"),
                heading=f"Card {index}",
            )
        )

    sections = []
    for index in range(0, card_count, 10):
        sections.append(
            dashboard_section(
                *cards[index:index + 10],
                title=f"Section {index // 10 + 1}",
            )
        )

    return Column(
        text("Large dashboard"),
        *sections,
        table(
            data=[[str(index), f"Row {index}", str(index * 10)] for index in range(50)],
            headers=["ID", "Name", "Value"],
        ),
    )


def _count_tree(component):
    count = 1
    for child in component.children:
        count += _count_tree(child)
    return count


def test_phase16_large_dashboard_behavior():
    iterations = 10
    dashboard = _build_large_dashboard()

    assert isinstance(dashboard, Component)

    tree_nodes = _count_tree(dashboard)
    assert tree_nodes >= 500

    renderer = HTMLRenderer()

    start = perf_counter()
    for _ in range(iterations):
        html = renderer.render(dashboard)
    elapsed = perf_counter() - start

    assert html
    assert "Large dashboard" in html
    assert "Metric 99" in html
    assert "Row 49" in html

    print()
    print("===== PHASE 16 — LARGE DASHBOARD BEHAVIOR =====")
    print(f"dashboard cards   : 100")
    print(f"table rows        : 50")
    print(f"tree nodes        : {tree_nodes}")
    print(f"render iterations  : {iterations}")
    print(f"total render      : {elapsed:.9f}s")
    print(f"per render        : {elapsed / iterations:.9f}s")
    print(f"html bytes        : {len(html.encode('utf-8'))}")

    assert elapsed >= 0
