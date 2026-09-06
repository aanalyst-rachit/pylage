import pytest

import pylage.UI as ps
from pylage.ENGINE import Style
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render


def test_button_returns_existing_component():
    button = ps.button("Save")

    assert isinstance(button, Component)
    assert button.type == "Button"
    assert button.props["text"] == "Save"


def test_button_default_contract():
    button = ps.button("Save")
    style = button.props["style"]

    assert style.background_color == "var(--color-primary)"
    assert style.color == "var(--color-primary-contrast)"
    assert style.border == "1px solid var(--color-primary)"
    assert style.border_radius == "var(--radius-lg)"
    assert style.font_weight == "600"
    assert style.padding == "0.625rem 1rem"
    assert style.font_size == "1rem"
    assert style.cursor == "pointer"


@pytest.mark.parametrize(
    ("variant", "background", "foreground", "border"),
    [
        ("primary", "var(--color-primary)", "var(--color-primary-contrast)", "1px solid var(--color-primary)"),
        ("secondary", "var(--color-secondary)", "var(--color-secondary-contrast)", "1px solid var(--color-secondary)"),
        ("outline", "var(--color-background)", "var(--color-primary-hover)", "1px solid var(--color-primary-hover)"),
        ("ghost", "transparent", "var(--color-text)", "1px solid transparent"),
        ("danger", "var(--color-danger)", "var(--color-primary-contrast)", "1px solid var(--color-danger)"),
    ],
)
def test_button_variants(variant, background, foreground, border):
    button = ps.button("Action", variant=variant)
    style = button.props["style"]

    assert style.background_color == background
    assert style.color == foreground
    assert style.border == border


@pytest.mark.parametrize(
    ("size", "padding", "font_size"),
    [
        ("sm", "0.5rem 0.75rem", "0.875rem"),
        ("md", "0.625rem 1rem", "1rem"),
        ("lg", "0.75rem 1.25rem", "1.125rem"),
    ],
)
def test_button_sizes(size, padding, font_size):
    button = ps.button("Action", size=size)
    style = button.props["style"]

    assert style.padding == padding
    assert style.font_size == font_size


def test_button_variant_size_and_local_style_precedence():
    button = ps.button(
        "Action",
        variant="danger",
        size="lg",
        style=Style(
            background_color="#123456",
            padding="2rem",
        ),
    )
    style = button.props["style"]

    # Local style wins over variant and size.
    assert style.background_color == "#123456"
    assert style.padding == "2rem"

    # Unrelated values from the selected variant remain intact.
    assert style.color == "var(--color-primary-contrast)"
    assert style.border == "1px solid var(--color-danger)"



def test_button_disabled_is_forwarded():
    button = ps.button("Save", disabled=True)

    assert button.props["disabled"] is True

    html = render(button)
    assert "disabled" in html
    assert ">Save</button>" in html


def test_button_event_is_forwarded():
    called = []

    def handle_click():
        called.append(True)

    button = ps.button("Save", on_click=handle_click)

    assert button.events["click"] is handle_click

    html = render(button)
    assert 'data-pylage-events="click"' in html
    assert "handle_click" not in html


def test_button_custom_style_overrides_defaults():
    custom = Style(
        background_color="#123456",
        padding="2rem",
        border_radius="999px",
    )

    button = ps.button("Custom", style=custom)
    style = button.props["style"]

    assert style.background_color == "#123456"
    assert style.padding == "2rem"
    assert style.border_radius == "999px"

    # Unspecified defaults remain available.
    assert style.font_weight == "600"
    assert style.cursor == "pointer"


@pytest.mark.parametrize("variant", ["", "invalid", "PRIMARY", "success"])
def test_button_rejects_unknown_variant(variant):
    with pytest.raises(ValueError, match="Unknown button variant"):
        ps.button("Action", variant=variant)


@pytest.mark.parametrize("size", ["", "xl", "medium", "INVALID"])
def test_button_rejects_unknown_size(size):
    with pytest.raises(ValueError, match="Unknown button size"):
        ps.button("Action", size=size)


def test_button_does_not_leak_ui_kit_props_to_engine():
    button = ps.button("Save", variant="danger", size="lg")

    assert "variant" not in button.props
    assert "size" not in button.props
