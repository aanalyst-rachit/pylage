from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.registry import ComponentRegistry, PropDefinition
from pylage.ENGINE.core.renderer import HTMLRenderer
from pylage.ENGINE.core.state import State


def test_registry_dom_metadata():
    registry = ComponentRegistry()

    registry.register(
        "TestButton",
        "button",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "disabled": PropDefinition(
                "disabled",
                kind="boolean",
                html_name="disabled",
            ),
            "visible": PropDefinition(
                "visible",
                kind="boolean",
                html_name="hidden",
                boolean_mode="inverse",
            ),
            "label": PropDefinition(
                "label",
                kind="text",
            ),
        },
    )

    definition = registry.get("TestButton")

    assert definition is not None
    assert definition.props["class_name"].html_name == "class"
    assert definition.props["disabled"].kind == "boolean"

    visible_prop = definition.props["visible"]
    assert visible_prop.kind == "boolean"
    assert visible_prop.html_name == "hidden"
    assert visible_prop.boolean_mode == "inverse"

    assert definition.props["label"].kind == "text"

    component = Component(
        type="TestButton",
        props={
            "class_name": State("active"),
            "disabled": State(False),
            "visible": State(True),
            "label": State("Save"),
        },
    )

    class_prop = definition.props["class_name"]
    disabled_prop = definition.props["disabled"]
    visible_prop = definition.props["visible"]
    label_prop = definition.props["label"]

    assert class_prop.html_name == "class"
    assert disabled_prop.html_name == "disabled"
    assert visible_prop.html_name == "hidden"
    assert visible_prop.boolean_mode == "inverse"
    assert label_prop.html_name is None

    assert component.props["visible"].value is True


    print("Registry metadata contract: PASS")
