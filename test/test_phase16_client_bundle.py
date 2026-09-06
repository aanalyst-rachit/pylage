from pylage.ENGINE import Button, Column, Text
from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.ENGINE.runtime.client import get_client_runtime
from pylage.UI.components.button import button
from pylage.UI.components.text import text


def _render(component):
    return HTMLRenderer().render(component)


def test_phase16_client_bundle_impact():
    core_page = Column(
        Button("Save"),
        Text(text="Dashboard"),
    )
    ui_kit_page = Column(
        button("Save"),
        text("Dashboard"),
    )

    core_html = _render(core_page)
    ui_kit_html = _render(ui_kit_page)

    core_runtime = get_client_runtime()
    ui_kit_runtime = get_client_runtime()

    core_size = len(core_html.encode("utf-8"))
    ui_kit_size = len(ui_kit_html.encode("utf-8"))
    core_runtime_size = len(core_runtime.encode("utf-8"))
    ui_kit_runtime_size = len(ui_kit_runtime.encode("utf-8"))

    assert core_html
    assert ui_kit_html
    assert core_runtime
    assert ui_kit_runtime
    assert core_runtime == ui_kit_runtime
    assert "window.PyLage" in core_runtime
    assert "window.PyLage" in ui_kit_runtime
    assert core_runtime_size == ui_kit_runtime_size

    print()
    print("===== PHASE 16 — CLIENT / BUNDLE IMPACT =====")
    print()
    print(f"core html bytes       : {core_size}")
    print(f"ui kit html bytes     : {ui_kit_size}")
    print(f"html byte difference  : {ui_kit_size - core_size}")
    print(f"core runtime bytes    : {core_runtime_size}")
    print(f"ui kit runtime bytes  : {ui_kit_runtime_size}")
    print(f"runtime identical     : {core_runtime == ui_kit_runtime}")
    print()
