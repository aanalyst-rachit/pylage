from time import perf_counter

from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.UI.components.table import table


def _build_large_table(row_count=1000, column_count=10):
    headers = [f"Column {index}" for index in range(column_count)]
    data = [
        [f"R{row}C{column}" for column in range(column_count)]
        for row in range(row_count)
    ]
    return table(data=data, headers=headers)


def test_phase16_large_table_behavior():
    iterations = 10
    row_count = 1000
    column_count = 10

    large_table = _build_large_table(row_count, column_count)

    assert isinstance(large_table, Component)

    renderer = HTMLRenderer()

    start = perf_counter()
    for _ in range(iterations):
        html = renderer.render(large_table)
    elapsed = perf_counter() - start

    assert html
    assert "Column 0" in html
    assert "Column 9" in html
    assert "R0C0" in html
    assert "R999C9" in html

    print()
    print("===== PHASE 16 — LARGE TABLE BEHAVIOR =====")
    print(f"table rows        : {row_count}")
    print(f"table columns     : {column_count}")
    print(f"render iterations  : {iterations}")
    print(f"total render      : {elapsed:.9f}s")
    print(f"per render        : {elapsed / iterations:.9f}s")
    print(f"html bytes        : {len(html.encode('utf-8'))}")

    assert elapsed >= 0
