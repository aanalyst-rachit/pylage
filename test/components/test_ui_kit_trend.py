from pylage.ENGINE import Badge as EngineBadge
from pylage.ENGINE import State, Style
from pylage.ENGINE.core.renderer import render

import pylage.UI as ui


def test_trend_returns_existing_badge_component():
    trend = ui.trend("+12%")

    assert trend.type == "Badge"
    assert isinstance(trend, type(EngineBadge()))


def test_trend_auto_detects_up_direction():
    trend = ui.trend("+12%")
    html = render(trend)
    style = trend.props["style"]

    assert "↑" in html
    assert "+12%" in html
    assert style.background_color == "var(--color-success)"


def test_trend_auto_detects_down_direction():
    trend = ui.trend("-8%")
    html = render(trend)
    style = trend.props["style"]

    assert "↓" in html
    assert "-8%" in html
    assert style.background_color == "var(--color-danger)"


def test_trend_defaults_to_neutral_direction():
    trend = ui.trend("0%")
    html = render(trend)
    style = trend.props["style"]

    assert "→" in html
    assert "0%" in html
    assert style.background_color == "var(--color-secondary)"


def test_trend_supports_explicit_direction():
    trend = ui.trend(
        "Improving",
        direction="up",
    )

    html = render(trend)

    assert "↑" in html
    assert "Improving" in html


def test_trend_can_hide_indicator():
    html = render(
        ui.trend(
            "+12%",
            show_indicator=False,
        )
    )

    assert "+12%" in html
    assert "↑" not in html


def test_trend_supports_state_values():
    value = State("+12%")

    html = render(ui.trend(value))

    assert "+12%" in html


def test_trend_custom_style_overrides_defaults():
    trend = ui.trend(
        "+12%",
        style=Style(
            background_color="#111827",
            padding="0.5rem 1rem",
        ),
    )

    style = trend.props["style"]

    assert style.background_color == "#111827"
    assert style.padding == "0.5rem 1rem"
    assert style.border_radius == "var(--radius-full)"


def test_trend_forwards_engine_props_and_events():
    clicked = []

    trend = ui.trend(
        "+12%",
        class_name="revenue-trend",
        title="Revenue trend",
        on_click=lambda: clicked.append(True),
    )

    assert "click" in trend.events

    html = render(trend)

    assert 'class="revenue-trend"' in html
    assert 'title="Revenue trend"' in html
    assert 'data-pylage-events="click"' in html


def test_trend_does_not_leak_semantic_props():
    trend = ui.trend(
        "+12%",
        direction="up",
        show_indicator=False,
    )

    assert "direction" not in trend.props
    assert "show_indicator" not in trend.props


def test_trend_rejects_unknown_direction():
    try:
        ui.trend("+12%", direction="sideways")
    except ValueError as exc:
        assert "Unknown trend direction" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
