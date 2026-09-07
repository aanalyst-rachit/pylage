from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.registry import registry
from pylage.ENGINE.core.renderer import render


print("=== PYLAGE REGISTRY VOID TEST ===")

registry.register("RawInput", "input", void=True)

component = Component(
    type="RawInput",
    props={
        "value": "Dollar",
        "title": "Test input",
    },
)

html = render(component)

print(html)

assert "<input" in html
assert 'value="Dollar"' in html
assert 'title="Test input"' in html
assert "</input>" not in html

definition = registry.require("RawInput")

assert definition.tag == "input"
assert definition.void is True

print("Void definition: PASS")
print("Void rendering: PASS")
print("No closing tag: PASS")
print()
print("=== REGISTRY VOID PASS ===")
