from pylage.ENGINE import Card as EngineCard
from pylage.ENGINE import Style, State
from pylage.ENGINE.core.renderer import render

import pylage.UI as ui


def test_metric_returns_existing_metric_card():
    metric = ui.metric(label="Revenue", value="₹42,000")

    assert metric.type == "Card"
    assert isinstance(metric, type(EngineCard()))


def test_metric_default_style_contract():
    metric = ui.metric(label="Revenue", value="₹42,000")
    style = metric.props["style"]

    assert style.background_color == "var(--color-background)"
    assert style.padding == "var(--spacing-lg)"
    assert style.border_radius == "var(--radius-xl)"
    assert style.border == "1px solid var(--color-border)"


def test_metric_renders_semantic_content():
    html = render(ui.metric(
        label="Revenue",
        value="₹42,000",
        delta="+12%",
        description="vs last month",
    ))

    assert "Revenue" in html
    assert "₹42,000" in html
    assert "+12%" in html
    assert "vs last month" in html


def test_metric_supports_state_values():
    value = State("42,000")
    delta = State("+12%")

    metric = ui.metric(
        label="Revenue",
        value=value,
        delta=delta,
    )

    html = render(metric)
    assert "42,000" in html
    assert "+12%" in html


def test_metric_custom_style_overrides_defaults():
    metric = ui.metric(
        label="Revenue",
        value="₹42,000",
        style=Style(padding="2rem", border="2px solid #111827"),
    )

    style = metric.props["style"]

    assert style.padding == "2rem"
    assert style.border == "2px solid #111827"
    assert style.background_color == "var(--color-background)"


def test_metric_forwards_engine_props():
    metric = ui.metric(
        label="Revenue",
        value="₹42,000",
        class_name="revenue-metric",
        title="Monthly revenue",
    )

    html = render(metric)

    assert "revenue-metric" in html
    assert "Monthly revenue" in html


def test_metric_forwards_events():
    metric = ui.metric(
        label="Revenue",
        value="₹42,000",
        on_click=lambda: None,
    )

    assert "click" in metric.events
    assert "data-pylage-events" in render(metric)


def test_metric_style_is_not_leaked_as_none():
    metric = ui.metric(label="Revenue", value="₹42,000")
    assert metric.props["style"] is not None
