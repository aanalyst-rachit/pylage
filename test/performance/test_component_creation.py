from time import perf_counter

from pylage.ENGINE import Button, Text
from pylage.ENGINE.core.component import Component
from pylage.UI.components.button import button
from pylage.UI.components.card import card
from pylage.UI.components.table import table
from pylage.UI.components.text import text


def _measure(factory, iterations=1000):
    start = perf_counter()

    for _ in range(iterations):
        component = factory()
        assert isinstance(component, Component)

    elapsed = perf_counter() - start

    return {
        "total": elapsed,
        "per_operation": elapsed / iterations,
    }


def test_phase16_component_creation_overhead():
    iterations = 1000

    results = {
        "ui_button": _measure(
            lambda: button("Save"),
            iterations,
        ),
        "ui_text": _measure(
            lambda: text("Hello"),
            iterations,
        ),
        "ui_card": _measure(
            lambda: card(body="Hello"),
            iterations,
        ),
        "ui_table": _measure(
            lambda: table(
                data=[["A", "B"], ["C", "D"]],
                headers=["One", "Two"],
            ),
            iterations,
        ),
        "core_button": _measure(
            lambda: Button("Save"),
            iterations,
        ),
        "core_text": _measure(
            lambda: Text("Hello"),
            iterations,
        ),
    }

    print()
    print("===== PHASE 16 — COMPONENT CREATION OVERHEAD =====")
    print(f"iterations        : {iterations}")
    print()

    for name, result in results.items():
        print(name)
        print(f"  total           : {result['total']:.9f}s")
        print(f"  per component   : {result['per_operation']:.9f}s")
        print()

    for result in results.values():
        assert result["total"] >= 0
        assert result["per_operation"] >= 0
