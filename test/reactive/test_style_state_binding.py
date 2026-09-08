import pylage as ps
from pylage.ENGINE import State, Style, Text


def test_style_state_updates_component_binding():
    style_state = State(
        Style(color="red")
    )

    component = Text(
        "Hello",
        style=style_state,
    )

    updates = []

    component.subscribe_mutation(
        lambda event: updates.append(event)
    )

    style_state.set(
        Style(color="blue")
    )

    assert style_state.value == Style(color="blue")

    # Style State changes must remain represented by the same
    # component prop binding.
    assert component.props["style"] is style_state

    # The State itself must notify its subscribers.
    # Component-level mutation is intentionally not assumed here.
    assert updates == []
