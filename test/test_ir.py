import copy

import pytest

from pyskin.core.ir import IRNode, snapshot_to_ir


def test_irnode_construction():
    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
    )

    assert node.node_id == "1"
    assert node.node_type == "component"
    assert node.component_id == "Button"
    assert node.props == {"class": "primary"}

    assert len(node.children) == 1
    assert node.children[0].node_id == "2"
    assert node.children[0].component_id == "Text"
    assert node.children[0].props == {"text": "Hello"}


def test_stable_node_identity():
    node1 = IRNode(
        node_id="stable-id",
        node_type="component",
        component_id="Button",
    )

    node2 = IRNode(
        node_id="stable-id",
        node_type="component",
        component_id="Button",
    )

    assert node1.node_id == node2.node_id


def test_valid_node_type():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
    )

    assert node.node_type == "component"


def test_invalid_node_type_rejected():
    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="invalid",
            component_id="Button",
        )


def test_node_id_validation():
    with pytest.raises(ValueError):
        IRNode(
            node_id="",
            node_type="component",
            component_id="Button",
        )

    with pytest.raises(ValueError):
        IRNode(
            node_id=123,
            node_type="component",
            component_id="Button",
        )


def test_component_id_validation():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
    )

    assert node.component_id == "Button"

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="",
        )

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id=123,
        )


def test_props_validation():
    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={"text": "Hello"},
    )

    assert node.props == {"text": "Hello"}

    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Button",
            props="invalid",
        )


def test_props_are_copied():
    props = {
        "data": {
            "items": ["one", "two"],
        }
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props=props,
    )

    props["data"]["items"].append("three")

    assert node.props == {
        "data": {
            "items": ["one", "two"],
        }
    }


def test_child_insertion():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    parent.add_child(child)

    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_invalid_child_rejection():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    with pytest.raises(ValueError):
        parent.add_child("not-an-ir-node")


def test_children_validation():
    with pytest.raises(ValueError):
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Column",
            children=["invalid-child"],
        )


def test_deterministic_child_ordering():
    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
    )

    child1 = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    child2 = IRNode(
        node_id="3",
        node_type="component",
        component_id="Button",
    )

    parent.add_child(child1)
    parent.add_child(child2)

    assert [child.node_id for child in parent.children] == [
        "2",
        "3",
    ]


def test_children_list_is_copied():
    child = IRNode(
        node_id="2",
        node_type="component",
        component_id="Text",
    )

    children = [child]

    parent = IRNode(
        node_id="1",
        node_type="component",
        component_id="Column",
        children=children,
    )

    children.clear()

    assert len(parent.children) == 1
    assert parent.children[0] is child


def test_style_ref_is_opaque():
    style_ref = {
        "style_id": "style-1",
        "source": "phase9",
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        style_ref=style_ref,
    )

    assert node.style_ref is style_ref


def test_snapshot_to_ir_conversion():
    snapshot = {
        "id": "root",
        "type": "Button",
        "tag": "button",
        "events": "",
        "props": {
            "text": "Click me",
            "disabled": False,
        },
        "children": [
            {
                "id": "child",
                "type": "Text",
                "tag": "div",
                "events": "",
                "props": {
                    "text": "Hello",
                },
                "children": [],
            }
        ],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.node_id == "root"
    assert ir_node.node_type == "component"
    assert ir_node.component_id == "Button"

    assert ir_node.props == {
        "text": "Click me",
        "disabled": False,
    }

    assert len(ir_node.children) == 1

    child = ir_node.children[0]

    assert child.node_id == "child"
    assert child.node_type == "component"
    assert child.component_id == "Text"
    assert child.props == {
        "text": "Hello",
    }


def test_snapshot_to_ir_uses_component_type_not_html_tag():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {},
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.component_id == "Button"
    assert ir_node.component_id != snapshot["tag"]


def test_snapshot_to_ir_preserves_child_order():
    snapshot = {
        "id": "root",
        "type": "Column",
        "tag": "div",
        "props": {},
        "children": [
            {
                "id": "first",
                "type": "Text",
                "tag": "div",
                "props": {},
                "children": [],
            },
            {
                "id": "second",
                "type": "Button",
                "tag": "button",
                "props": {},
                "children": [],
            },
        ],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert [child.node_id for child in ir_node.children] == [
        "first",
        "second",
    ]


def test_snapshot_to_ir_does_not_modify_snapshot():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "data": {
                "items": ["one"],
            }
        },
        "children": [],
    }

    original = copy.deepcopy(snapshot)

    snapshot_to_ir(snapshot)

    assert snapshot == original


def test_snapshot_to_ir_deep_copies_props():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "data": {
                "items": ["one"],
            }
        },
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    snapshot["props"]["data"]["items"].append("changed")

    assert ir_node.props == {
        "data": {
            "items": ["one"],
        }
    }


def test_snapshot_to_ir_rejects_invalid_snapshot():
    with pytest.raises(TypeError):
        snapshot_to_ir("invalid")

    with pytest.raises(ValueError):
        snapshot_to_ir({})

    with pytest.raises(ValueError):
        snapshot_to_ir({
            "id": "1",
        })


def test_snapshot_to_ir_requires_children_list():
    snapshot = {
        "id": "1",
        "type": "Button",
        "props": {},
        "children": "invalid",
    }

    with pytest.raises(ValueError):
        snapshot_to_ir(snapshot)


def test_no_runtime_evaluation():
    snapshot = {
        "id": "1",
        "type": "Button",
        "tag": "button",
        "props": {
            "text": "Hello",
        },
        "children": [],
    }

    ir_node = snapshot_to_ir(snapshot)

    assert ir_node.component_id == "Button"
    assert ir_node.style_ref is None


def test_normalize_ir_preserves_identity_and_structure():
    from pyskin.core.ir import normalize_ir

    child = IRNode(
        node_id="child",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
        style_ref="style-ref",
    )

    normalized = normalize_ir(node)

    assert normalized is not node
    assert normalized.node_id == "root"
    assert normalized.node_type == "component"
    assert normalized.component_id == "Button"
    assert normalized.props == {"class": "primary"}
    assert normalized.style_ref == "style-ref"

    assert len(normalized.children) == 1
    assert normalized.children[0] is not child
    assert normalized.children[0].node_id == "child"
    assert normalized.children[0].component_id == "Text"


def test_normalize_ir_preserves_child_order():
    from pyskin.core.ir import normalize_ir

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=[
            IRNode(
                node_id="a",
                node_type="component",
                component_id="Text",
            ),
            IRNode(
                node_id="b",
                node_type="component",
                component_id="Button",
            ),
            IRNode(
                node_id="c",
                node_type="component",
                component_id="Input",
            ),
        ],
    )

    normalized = normalize_ir(node)

    assert [child.node_id for child in normalized.children] == [
        "a",
        "b",
        "c",
    ]


def test_normalize_ir_deep_copies_props():
    from pyskin.core.ir import normalize_ir

    props = {
        "metadata": {
            "items": ["one", "two"],
        },
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props=props,
    )

    normalized = normalize_ir(node)

    props["metadata"]["items"].append("three")

    assert normalized.props == {
        "metadata": {
            "items": ["one", "two"],
        },
    }


def test_normalize_ir_does_not_mutate_source():
    from pyskin.core.ir import normalize_ir

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        props={
            "metadata": {
                "enabled": True,
            },
        },
    )

    original_props = copy.deepcopy(node.props)
    original_children = list(node.children)

    normalize_ir(node)

    assert node.props == original_props
    assert node.children == original_children


def test_normalize_ir_preserves_opaque_style_ref():
    from pyskin.core.ir import normalize_ir

    style_ref = {
        "name": "button-style",
        "version": 1,
    }

    node = IRNode(
        node_id="1",
        node_type="component",
        component_id="Button",
        style_ref=style_ref,
    )

    normalized = normalize_ir(node)

    assert normalized.style_ref == style_ref
    assert normalized.style_ref is not style_ref


def test_normalize_ir_rejects_non_ir_node():
    from pyskin.core.ir import normalize_ir

    with pytest.raises(TypeError):
        normalize_ir("not an IR node")


def test_normalize_ir_preserves_identity_and_structure():
    from pyskin.core.ir import normalize_ir

    child = IRNode(
        node_id="child",
        node_type="component",
        component_id="Text",
        props={"text": "Hello"},
    )

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props={"class": "primary"},
        children=[child],
        style_ref="style-ref",
    )

    normalized = normalize_ir(node)

    assert normalized is not node
    assert normalized.node_id == "root"
    assert normalized.node_type == "component"
    assert normalized.component_id == "Button"
    assert normalized.props == {"class": "primary"}
    assert normalized.style_ref == "style-ref"

    assert len(normalized.children) == 1
    assert normalized.children[0] is not child
    assert normalized.children[0].node_id == "child"
    assert normalized.children[0].component_id == "Text"


def test_normalize_ir_rejects_invalid_input():
    from pyskin.core.ir import normalize_ir

    with pytest.raises(TypeError):
        normalize_ir("not an IR node")


def test_normalize_ir_deep_copies_props():
    from pyskin.core.ir import normalize_ir

    props = {
        "metadata": {
            "items": ["one", "two"],
        }
    }

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Button",
        props=props,
    )

    normalized = normalize_ir(node)

    props["metadata"]["items"].append("three")

    assert normalized.props == {
        "metadata": {
            "items": ["one", "two"],
        }
    }


def test_normalize_ir_preserves_child_order():
    from pyskin.core.ir import normalize_ir

    children = [
        IRNode(
            node_id="1",
            node_type="component",
            component_id="Text",
            props={"text": "One"},
        ),
        IRNode(
            node_id="2",
            node_type="component",
            component_id="Text",
            props={"text": "Two"},
        ),
    ]

    node = IRNode(
        node_id="root",
        node_type="component",
        component_id="Column",
        children=children,
    )

    normalized = normalize_ir(node)

    assert [child.node_id for child in normalized.children] == ["1", "2"]
