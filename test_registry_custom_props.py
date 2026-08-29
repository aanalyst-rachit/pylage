from pyskin.core.component import Component
from pyskin.core.registry import PropDefinition, registry
from pyskin.core.renderer import HTMLRenderer


print("=== PYSKIN CUSTOM REGISTRY PROP RENDERING TEST ===")


# ---------------------------------------------------------
# Register a custom component with registry-defined props
# ---------------------------------------------------------
registry.register(
    "Card",
    "section",
    props={
        "label": PropDefinition(
            "label",
            kind="text",
        ),
        "class_name": PropDefinition(
            "class_name",
            kind="attribute",
            html_name="class",
        ),
        "hidden": PropDefinition(
            "hidden",
            kind="boolean",
            html_name="hidden",
        ),
        "data_id": PropDefinition(
            "data_id",
            kind="attribute",
            html_name="data-id",
        ),
    },
)


card = Component(
    type="Card",
    props={
        "label": "Hello Card",
        "class_name": "premium-card",
        "hidden": True,
        "data_id": "card-01",
    },
)


html = HTMLRenderer().render(card)

print(html)

assert "<section" in html
assert "Hello Card" in html
assert 'class="premium-card"' in html
assert "hidden" in html
assert 'data-id="card-01"' in html

print("Registry HTML names: PASS")
print("Registry boolean props: PASS")
print("Registry custom attributes: PASS")


# ---------------------------------------------------------
# Cleanup
# ---------------------------------------------------------
registry.unregister("Card")

print()
print("=== CUSTOM REGISTRY PROP RENDERING PASS ===")
