from pylage.ENGINE.core.state import State

from playground import get_app


def _find_components(root, type_name):
    found = []

    def visit(component):
        if getattr(component, "type", None) == type_name:
            found.append(component)
        for child in getattr(component, "children", []):
            visit(child)

    visit(root)
    return found


def test_playground_builds_with_editor_preview_and_run_button():
    app = get_app()

    textareas = _find_components(app, "Textarea")
    buttons = _find_components(app, "Button")

    assert len(textareas) == 1
    assert any(button.props.get("text") == "Run" for button in buttons)


def test_playground_editor_is_bound_to_state():
    app = get_app()

    textarea = _find_components(app, "Textarea")[0]

    assert isinstance(textarea.props["value"], State)


def test_playground_run_updates_preview_from_editor_state():
    app = get_app()

    buttons = _find_components(app, "Button")
    run_button = next(button for button in buttons if button.props.get("text") == "Run")

    textarea = _find_components(app, "Textarea")[0]
    state = textarea.props["value"]
    state.set("pl.text(\\\"Updated from test\\\")")

    preview = next(
        component
        for component in _find_components(app, "Card")
        if any(
            getattr(child, "type", None) == "Heading"
            and child.props.get("text") == "Live Preview"
            for child in component.children
        )
    )

    mutations = []
    preview.subscribe_mutation(lambda event: mutations.append(event))

    handler = run_button.events["click"]
    handler()

    assert len(mutations) == 1
    event = mutations[0]
    assert event["type"] == "set_children"
    assert event["parent"] is preview
    assert any(
        getattr(child, "type", None) == "Text"
        and child.props.get("text") == "Preview updated from the editor."
        for child in event["children"]
    )
