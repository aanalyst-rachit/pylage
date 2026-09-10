from playground.app import get_app
from playground.runtime import PYLAGE_WHEEL, PYODIDE_VERSION, build_playground_document


def test_playground_document_contains_browser_runtime_hooks():
    document = build_playground_document(get_app())

    assert f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js" in document
    assert f"/dist/{PYLAGE_WHEEL}" in document

    deployment_document = build_playground_document(
        get_app(),
        wheel_url=f"../dist/{PYLAGE_WHEEL}",
    )
    assert f"../dist/{PYLAGE_WHEEL}" in deployment_document
    assert 'pylage-playground-editor' in document
    assert 'pylage-playground-run' in document
    assert 'pylage-playground-preview' in document
    assert 'pylage-playground-status' in document


def test_playground_browser_runtime_executes_pylage_component_code():
    document = build_playground_document(get_app())

    assert 'await pyodide.runPythonAsync' in document
    assert 'from pylage.ENGINE.core.component import Component' in document
    assert 'from pylage.ENGINE.core.renderer import render' in document
    assert 'preview.innerHTML = html' in document

def test_playground_header_actions_are_exposed():
    document = build_playground_document(get_app())

    assert "pylage-playground-docs" in document
    assert "pylage-playground-github" in document
    assert "pylage-playground-install" in document
    assert "https://aanalyst-rachit.github.io/pylage/" in document
    assert "https://github.com/aanalyst-rachit/pylage" in document
    assert "pip install pylage" in document
