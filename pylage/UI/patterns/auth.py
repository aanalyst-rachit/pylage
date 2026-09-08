"""Authentication patterns for PyLage Layout."""

from typing import Any, Callable

from pylage.ENGINE.components import Button, Column, Form, Heading, Input, Text


def LoginForm(
    title: Any = "Login",
    button_text: Any = "Login",
    *,
    on_submit: Callable[[Any], Any] | None = None,
    class_name: str = "login-form",
    **props: Any,
):
    """Create a reusable login form."""
    btn_props = {}
    if on_submit is not None:
        btn_props["on_click"] = on_submit

    return Column(
        Heading(title),
        Form(
            Input(placeholder="Email", type="email", class_name="auth-input-email"),
            Input(placeholder="Password", type="password", class_name="auth-input-password"),
            Button(button_text, **btn_props, class_name="auth-submit-btn"),
            class_name="auth-form-body",
        ),
        class_name=class_name,
        **props,
    )


def SignupForm(
    title: Any = "Create Account",
    button_text: Any = "Sign Up",
    *,
    on_submit: Callable[[Any], Any] | None = None,
    class_name: str = "signup-form",
    **props: Any,
):
    """Create a reusable signup form."""
    btn_props = {}
    if on_submit is not None:
        btn_props["on_click"] = on_submit

    return Column(
        Heading(title),
        Form(
            Input(placeholder="Name", class_name="auth-input-name"),
            Input(placeholder="Email", type="email", class_name="auth-input-email"),
            Input(placeholder="Password", type="password", class_name="auth-input-password"),
            Button(button_text, **btn_props, class_name="auth-submit-btn"),
            class_name="auth-form-body",
        ),
        class_name=class_name,
        **props,
    )
