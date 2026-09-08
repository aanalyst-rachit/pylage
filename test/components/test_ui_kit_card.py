from pylage.ENGINE import Card as EngineCard
from pylage.ENGINE import Style, Text
from pylage.ENGINE.core.renderer import render

import pylage.UI as ui


def test_card_returns_existing_card_component():
    card = ui.card()
    assert card.type == "Card"
    assert isinstance(card, type(EngineCard()))


def test_card_default_style_contract():
    card = ui.card()
    style = card.props["style"]

    assert style.background_color == "var(--color-background)"
    assert style.padding == "var(--spacing-lg)"
    assert style.border_radius == "var(--radius-xl)"
    assert style.border == "1px solid var(--color-border)"


def test_card_supports_heading_body_footer():
    card = ui.card(
        heading="Rachit",
        body="Good work",
        footer="10% above ↑",
    )

    html = render(card)

    assert "Rachit" in html
    assert "Good work" in html
    assert "10% above" in html


def test_card_sections_are_optional():
    card = ui.card(
        heading="Revenue",
        body="₹42,000",
    )

    html = render(card)

    assert "Revenue" in html
    assert "₹42,000" in html


def test_card_body_only():
    card = ui.card(body="Nothing to show")

    html = render(card)

    assert "Nothing to show" in html


def test_card_default_variant_is_used():
    card = ui.card()

    style = card.props["style"]

    assert style.box_shadow is None
    assert style.cursor is None


def test_card_elevated_variant():
    card = ui.card(variant="elevated")

    style = card.props["style"]

    assert style.background_color == "var(--color-background)"
    assert style.padding == "var(--spacing-lg)"
    assert style.border_radius == "var(--radius-xl)"
    assert style.border == "1px solid var(--color-border-muted)"
    assert style.box_shadow == "0 10px 15px -3px rgba(0,0,0,0.1)"


def test_card_outlined_variant():
    card = ui.card(variant="outlined")

    style = card.props["style"]

    assert style.background_color == "var(--color-background)"
    assert style.border == "1px solid var(--color-border-muted)"
    assert style.border_radius == "var(--radius-xl)"


def test_card_interactive_variant():
    card = ui.card(variant="interactive")

    style = card.props["style"]

    assert style.background_color == "var(--color-background)"
    assert style.border == "1px solid var(--color-border)"
    assert style.border_radius == "var(--radius-xl)"
    assert style.cursor == "pointer"


def test_card_custom_style_overrides_defaults():
    custom = Style(
        background_color="#111827",
        padding="2rem",
        border_radius="1rem",
    )

    card = ui.card(
        heading="Rachit",
        body="Good work",
        style=custom,
    )

    style = card.props["style"]

    assert style.background_color == "#111827"
    assert style.padding == "2rem"
    assert style.border_radius == "1rem"
    assert style.border == "1px solid var(--color-border)"


def test_card_variant_and_local_style_precedence():
    card = ui.card(
        variant="elevated",
        style=Style(
            background_color="#111827",
            border_radius="2rem",
        ),
    )
    style = card.props["style"]

    # Local style wins over the selected variant.
    assert style.background_color == "#111827"
    assert style.border_radius == "2rem"

    # Unrelated elevated variant values remain intact.
    assert style.border == "1px solid var(--color-border-muted)"
    assert style.box_shadow == "0 10px 15px -3px rgba(0,0,0,0.1)"



def test_card_forwards_events():
    clicked = []

    def on_click():
        clicked.append(True)

    card = ui.card(
        heading="Click me",
        body="Interactive",
        on_click=on_click,
    )

    assert "click" in card.events

    html = render(card)

    assert 'data-pylage-events="click"' in html


def test_card_accepts_advanced_children():
    card = ui.card(
        Text("Advanced content"),
        variant="elevated",
    )

    html = render(card)

    assert "Advanced content" in html


def test_card_variant_is_not_leaked_to_engine_props():
    card = ui.card(
        heading="Rachit",
        variant="elevated",
    )

    assert "variant" not in card.props


def test_card_rejects_unknown_variant():
    try:
        ui.card(variant="unknown")
    except ValueError as exc:
        assert "Unknown card variant" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
