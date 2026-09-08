"""Contact section pattern for PyLage Layout."""

from typing import Any, Callable

from pylage.ENGINE.components import Button, Column, Form, Heading, Input, Text


def ContactSection(
    title: Any = "Contact Us",
    description: Any = "Get in touch with us.",
    button_text: Any = "Send Message",
    *,
    on_submit: Callable[[Any], Any] | None = None,
    class_name: str = "contact-section",
    **props: Any,
):
    """Create a reusable contact section using PyLage components."""
    btn_props = {}
    if on_submit is not None:
        btn_props["on_click"] = on_submit

    return Column(
        Heading(title),
        Text(description),
        Form(
            Input(placeholder="Your Name", class_name="contact-input-name"),
            Input(placeholder="Your Email", type="email", class_name="contact-input-email"),
            Input(placeholder="Your Message", class_name="contact-input-msg"),
            Button(button_text, **btn_props, class_name="contact-submit-btn"),
            class_name="contact-form",
        ),
        class_name=class_name,
        **props,
    )
