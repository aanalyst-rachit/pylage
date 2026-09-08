from pylage.ENGINE import Style
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render
from pylage.UI.components.alert import alert


def test_alert_wraps_existing_engine_alert():
    component = alert("Hello")

    assert isinstance(component, Component)
    assert component.type == "Alert"


def test_alert_renders_text():
    html = render(alert("Something happened"))

    assert "Something happened" in html


def test_alert_supports_variants():
    for variant in (
        "default",
        "info",
        "success",
        "warning",
        "danger",
        "error",
    ):
        component = alert("Message", variant=variant)

        assert component.type == "Alert"
        assert "style" in component.props


def test_alert_rejects_unknown_variant():
    try:
        alert("Message", variant="unknown")
    except ValueError as exc:
        assert "Unknown alert variant" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_alert_forwards_title():
    component = alert(
        "Message",
        title="Notice",
    )

    assert component.props["title"] == "Notice"


def test_alert_forwards_engine_props():
    component = alert(
        "Message",
        class_name="custom-alert",
    )

    assert component.props["class_name"] == "custom-alert"


def test_alert_supports_custom_style_override():
    component = alert(
        "Message",
        variant="info",
        style=Style(
            padding="32px",
        ),
    )

    assert component.props["style"].padding == "32px"


def test_alert_preserves_component_children():
    child = Component("Text", children=["Child"])
    component = alert(child)

    assert component.children == [child]
