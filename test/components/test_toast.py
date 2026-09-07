from pylage.ENGINE import Toast
from pylage.ENGINE.core.renderer import render


def test_toast_renders_as_div():
    toast = Toast()

    html = render(toast)

    assert "<div" in html


def test_toast_supports_props():
    toast = Toast(
        class_name="success-toast",
        title="Success",
    )

    html = render(toast)

    assert 'class="success-toast"' in html
    assert 'title="Success"' in html


def test_toast_supports_text():
    toast = Toast(
        text="Saved successfully",
    )

    html = render(toast)

    assert "Saved successfully" in html

def test_toast_visible_false_renders_hidden_attribute():
    toast = Toast(visible=False)
    html = render(toast)
    opening_tag = html.split('<div', 1)[1].split('>', 1)[0]
    assert ' hidden' in opening_tag


def test_toast_visible_true_does_not_render_hidden_attribute():
    toast = Toast(visible=True)
    html = render(toast)
    opening_tag = html.split('<div', 1)[1].split('>', 1)[0]
    assert ' hidden' not in opening_tag


def test_render_includes_hidden_semantic_css():
    html = render(Toast(visible=False))
    assert '[hidden]' in html
    assert 'display: none ' + chr(33) + 'important' in html
