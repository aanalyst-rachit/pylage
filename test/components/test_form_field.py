import pylage as pl
from pylage.ENGINE.core.renderer import render


def test_form_field_wraps_existing_control():
    field = pl.form_field(
        pl.input(value="user@example.com"),
        label="Email",
    )

    assert field.type == "Column"
    assert len(field.children) == 2
    assert field.children[0].type == "Label"
    assert field.children[1].type == "Input"
    assert field.children[0].props["for"] == field.children[1].props["id"]


def test_form_field_renders_label_and_control():
    field = pl.form_field(
        pl.input(value="user@example.com"),
        label="Email",
    )

    html = render(field)

    assert "Email" in html
    assert "user@example.com" in html
    assert "<input" in html


def test_form_field_supports_help_text():
    field = pl.form_field(
        pl.textarea(),
        label="Message",
        help_text="Keep it concise.",
    )

    html = render(field)

    assert "Message" in html
    assert "Keep it concise." in html
    assert 'aria-describedby="pylage-field-help-' in html
    assert 'id="pylage-field-help-' in html


def test_form_field_supports_error():
    field = pl.form_field(
        pl.input(),
        label="Email",
        error="Invalid email address.",
    )

    html = render(field)

    assert "Invalid email address." in html
    assert 'aria-describedby="pylage-field-error-' in html
    assert 'aria-invalid' in html
    assert 'id="pylage-field-error-' in html


def test_form_field_required_marks_label():
    field = pl.form_field(
        pl.input(),
        label="Email",
        required=True,
    )

    html = render(field)

    assert "Email *" in html


def test_form_field_supports_custom_props():
    field = pl.form_field(
        pl.input(),
        label="Name",
        class_name="profile-field",
        title="Profile name",
    )

    html = render(field)

    assert "profile-field" in html
    assert "Profile name" in html


def test_form_field_preserves_existing_control_events():
    received = []

    field = pl.form_field(
        pl.input(
            value="hello",
            on_input=lambda payload: received.append(payload),
        ),
        label="Message",
    )

    assert "input" in field.children[1].events
    assert callable(field.children[1].events["input"])


def test_form_field_accepts_select_control():
    field = pl.form_field(
        pl.select(),
        label="Country",
    )

    assert field.type == "Column"
    assert field.children[0].type == "Label"
    assert field.children[1].type == "Select"
    assert field.children[0].props["for"] == field.children[1].props["id"]
