from pyskin.core.component import component
from pyskin.core.registry import ComponentRegistry, PropDefinition
from pyskin.core.renderer import HTMLRenderer


print("=== PYSKIN REGISTRY GENERIC TEXT CONTRACT TEST ===")


registry = ComponentRegistry()

registry.register(
    "Card",
    "section",
    props={
        "title": PropDefinition(
            "title",
            kind="text",
        ),
        "data_id": PropDefinition(
            "data_id",
            kind="attribute",
            html_name="data-id",
        ),
    },
)


renderer = HTMLRenderer()

# Temporarily use isolated registry.
renderer.registry._definitions = registry._definitions


card = component(
    "Card",
    title="Premium Card",
    data_id="card-01",
)

html = renderer.render(card)

print(html)


assert "<section" in html
assert "Premium Card" in html
assert 'data-id="card-01"' in html

print("Registry-defined text prop rendering: PASS")


# A second text prop must also work without any renderer
# changes or component-name-specific logic.
registry.register(
    "Panel",
    "article",
    props={
        "heading": PropDefinition(
            "heading",
            kind="text",
        ),
    },
)

panel = component(
    "Panel",
    heading="Dynamic Panel",
)

html = renderer.render(panel)

print(html)

assert "<article" in html
assert "Dynamic Panel" in html

print("Arbitrary registry text prop: PASS")


print()
print("=== REGISTRY GENERIC TEXT CONTRACT PASS ===")
