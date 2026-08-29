from pyskin.core.protocol import TreeAddMessage


def test_tree_add_message_round_trip():
    message = TreeAddMessage(
        parent_id="parent123",
        components=[
            {
                "id": "child456",
                "type": "Button",
                "props": {
                    "text": "Hello",
                },
                "children": [],
            }
        ],
    )

    assert message.type == "tree_add"

    encoded = message.to_json()
    decoded = TreeAddMessage.from_json(encoded)

    assert decoded == message


def test_tree_add_message_dict_contract():
    message = TreeAddMessage(
        parent_id="root123",
        components=[
            {
                "id": "button123",
                "type": "Button",
                "props": {
                    "text": "Click",
                },
                "children": [],
            }
        ],
    )

    assert message.to_dict() == {
        "type": "tree_add",
        "parent_id": "root123",
        "components": [
            {
                "id": "button123",
                "type": "Button",
                "props": {
                    "text": "Click",
                },
                "children": [],
            }
        ],
    }


def test_tree_add_message_requires_parent_id():
    try:
        TreeAddMessage(
            parent_id="",
            components=[],
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Empty parent_id must raise ValueError"
        )

def test_tree_add_message_preserves_nested_children():
    message = TreeAddMessage(
        parent_id="root123",
        components=[
            {
                "id": "column123",
                "type": "Column",
                "props": {},
                "children": [
                    {
                        "id": "button123",
                        "type": "Button",
                        "props": {
                            "text": "Nested",
                        },
                        "children": [],
                    }
                ],
            }
        ],
    )

    decoded = TreeAddMessage.from_json(message.to_json())

    assert decoded == message
    assert decoded.components[0]["children"][0]["id"] == "button123"

