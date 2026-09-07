from pylage import toast
from pylage.ENGINE import Style, Text
from pylage.ENGINE.core.component import Component
from pylage.ENGINE.core.renderer import render


def test_toast_returns_engine_toast_component():
    component = toast("Saved successfully")
    assert isinstance(component, Component)
    assert component.type == "Toast"


def test_toast_wraps_plain_text_children():
    component = toast("Saved successfully")
    assert len(component.children) == 1
    assert isinstance(component.children[0], Component)
    assert component.children[0].type == "Text"


def test_toast_preserves_component_children():
    child = Text("Saved successfully")
    component = toast(child)
    assert component.children == [child]


def test_toast_supports_semantic_variants():
    for variant in ("default", "info", "success", "warning", "danger", "error"):
        component = toast("Message", variant=variant)
        html = render(component)
        assert "<div" in html


def test_toast_rejects_unknown_variant():
    try:
        toast("Message", variant="unknown")
    except ValueError as exc:
        assert "Unknown toast variant" in str(exc)
    else:
        raise AssertionError("toast() accepted an unknown variant")


def test_toast_preserves_engine_props():
    component = toast(
        "Saved",
        visible=False,
        title="Success",
        on_close=lambda payload=None: None,
    )
    assert component.props["visible"] is False
    assert component.props["title"] == "Success"
    assert callable(component.events["close"])


def test_toast_preserves_click_event():
    def close_toast():
        pass

    component = toast(
        "Saved",
        on_click=close_toast,
    )

    assert component.events["click"] is close_toast


def test_toast_merges_custom_style():
    component = toast(
        "Saved",
        variant="success",
        style=Style(
            max_width="30rem",
            padding="2rem",
        ),
    )
    style = component.props["style"]
    assert style.max_width == "30rem"
    assert style.padding == "2rem"


def test_toast_renders_message():
    html = render(toast("Notification saved successfully."))
    assert "Notification saved successfully." in html
