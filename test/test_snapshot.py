from pyskin.core.component import Component
from pyskin.core.snapshot import component_to_snapshot


def test_component_to_snapshot_serializes_component():
    button = Component(
        type="Button",
        props={"text": "Hello"},
    )

    snapshot = component_to_snapshot(button)

    assert snapshot == {
        "id": button.id,
        "type": "Button",
        "tag": "button",
        "events": "",
        "props": {
            "text": "Hello",
        },
        "children": [],
    }


def test_component_to_snapshot_serializes_nested_children():
    root = Component(type="Column")

    child = Component(
        type="Button",
        props={"text": "Child"},
    )

    nested = Component(
        type="Text",
        props={"text": "Nested"},
    )

    child.add(nested)
    root.add(child)

    snapshot = component_to_snapshot(root)

    assert snapshot["id"] == root.id
    assert snapshot["type"] == "Column"
    assert snapshot["tag"] == "div"

    assert len(snapshot["children"]) == 1

    child_snapshot = snapshot["children"][0]

    assert child_snapshot["id"] == child.id
    assert child_snapshot["type"] == "Button"
    assert child_snapshot["tag"] == "button"

    assert len(child_snapshot["children"]) == 1

    nested_snapshot = child_snapshot["children"][0]

    assert nested_snapshot["id"] == nested.id
    assert nested_snapshot["type"] == "Text"
    assert nested_snapshot["tag"] == "div"


def test_component_to_snapshot_serializes_event_names():
    button = Component(type="Button")

    button.on("click", lambda: None)
    button.on("focus", lambda: None)

    snapshot = component_to_snapshot(button)

    assert snapshot["events"] == "click,focus"


def test_component_to_snapshot_ignores_non_component_children():
    root = Component(type="Column")

    root.add(
        "plain text",
        123,
        Component(type="Button"),
    )

    snapshot = component_to_snapshot(root)

    assert len(snapshot["children"]) == 1
    assert snapshot["children"][0]["type"] == "Button"


def test_component_to_snapshot_unknown_component_uses_div_tag():
    component = Component(
        type="UnknownComponent",
        props={"foo": "bar"},
    )

    snapshot = component_to_snapshot(component)

    assert snapshot["type"] == "UnknownComponent"
    assert snapshot["tag"] == "div"
    assert snapshot["props"] == {"foo": "bar"}
