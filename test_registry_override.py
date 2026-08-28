from pyskin.core.component import Component
from pyskin.core.registry import registry
from pyskin.core.renderer import render


print("=== PYSKIN REGISTRY OVERRIDE TEST ===")


def render_custom(renderer, component):
    return '<article data-custom="yes">CUSTOM</article>'


registry.register(
    "Heading",
    "article",
    renderer=render_custom,
)

heading = Component(
    type="Heading",
    props={"text": "Hello"},
)

html = render(heading)

print(html)

assert html == '<article data-custom="yes">CUSTOM</article>'

definition = registry.require("Heading")

assert definition.tag == "article"
assert definition.renderer is render_custom

print("Custom override preserved: PASS")
print()
print("=== REGISTRY OVERRIDE PASS ===")
