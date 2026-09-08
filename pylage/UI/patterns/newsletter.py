"""Newsletter pattern for PyLage Layout."""

from typing import Any, Callable

from pylage.ENGINE.components import Button, Column, Form, Heading, Input, Text


def NewsletterSection(
    title: Any = "Subscribe",
    description: Any = "Get the latest updates.",
    button_text: Any = "Subscribe",
    *,
    on_subscribe: Callable[[Any], Any] | None = None,
    class_name: str = "newsletter-section",
    **props: Any,
):
    """Create a reusable newsletter signup section."""
    btn_props = {}
    if on_subscribe is not None:
        btn_props["on_click"] = on_subscribe

    return Column(
        Heading(title),
        Text(description),
        Form(
            Input(placeholder="Enter your email", type="email", class_name="newsletter-input"),
            Button(button_text, **btn_props, class_name="newsletter-submit-btn"),
            class_name="newsletter-form",
        ),
        class_name=class_name,
        **props,
    )
