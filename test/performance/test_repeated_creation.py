from time import perf_counter

from pylage.ENGINE.core.component import Component
from pylage.UI.components.button import button
from pylage.UI.components.card import card
from pylage.UI.components.text import text


def _measure(factory, count):
    start = perf_counter()
    components = [factory(index) for index in range(count)]
    elapsed = perf_counter() - start
    return components, elapsed


def test_phase16_repeated_component_creation():
    print()
    print("===== PHASE 16 — REPEATED COMPONENT CREATION =====")
    print()

    for count in (10, 100, 1000, 10000):
        factories = {
            "ui_button": lambda index: button(f"Button {index}"),
            "ui_text": lambda index: text(f"Text {index}"),
            "ui_card": lambda index: card(body=f"Card {index}"),
        }

        for name, factory in factories.items():
            components, elapsed = _measure(factory, count)

            assert len(components) == count
            assert all(isinstance(component, Component) for component in components)
            assert len({id(component) for component in components}) == count
            assert len({component.id for component in components}) == count

            print(f"{name} ({count:5d})")
            print(f"  total             : {elapsed:.9f}s")
            print(f"  per component     : {elapsed / count:.9f}s")
            print()

        print("---")
