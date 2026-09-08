import pylage as ps
from pylage.ENGINE import Button


print("=== PYLAGE EVENT MODEL TEST ===")


calls = []


def clicked():
    calls.append("clicked")


button = Button(
    "Click me",
    on_click=clicked,
)


print("Type:", button.type)
print("Props:", button.props)
print("Events:", list(button.events))
print("Handler:", button.events["click"])


assert button.type == "Button"
assert button.props == {"text": "Click me"}
assert "click" in button.events
assert button.events["click"] is clicked


button.events["click"]()

print("Calls:", calls)

assert calls == ["clicked"]


print("=== EVENT MODEL PASS ===")
