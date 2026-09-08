from pylage.ENGINE import (
    Accordion,
    Audio,
    Avatar,
    Badge,
    Canvas,
    Card,
    Carousel,
    Icon,
    Image,
    Video,
)
from pylage.ENGINE.core.registry import registry


DYNAMIC_COMPONENTS = [
    "Card",
    "Badge",
    "Avatar",
    "Accordion",
    "Carousel",
    "Image",
    "Video",
    "Audio",
    "Icon",
    "Canvas",
]


ENGINE_COMPONENTS = {
    "Card": Card,
    "Badge": Badge,
    "Avatar": Avatar,
    "Accordion": Accordion,
    "Carousel": Carousel,
    "Image": Image,
    "Video": Video,
    "Audio": Audio,
    "Icon": Icon,
    "Canvas": Canvas,
}


def test_all_dynamic_components_are_central_registry_components():
    for name in DYNAMIC_COMPONENTS:
        assert registry.has(name), (
            f"{name} must exist in central registry"
        )


def test_dynamic_components_do_not_need_factory_registration():
    for name in DYNAMIC_COMPONENTS:
        factory = ENGINE_COMPONENTS[name]
        component = factory()
        assert component.type == name
        assert registry.has(component.type)


def test_central_registry_contains_unique_component_types():
    types = registry.types()
    assert len(types) == len(set(types))


def test_public_components_are_registry_backed():
    for name in DYNAMIC_COMPONENTS:
        factory = ENGINE_COMPONENTS[name]
        assert callable(factory)
        assert registry.has(name)
