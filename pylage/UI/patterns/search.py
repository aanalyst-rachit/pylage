"""Search pattern for PyLage Layout."""

from typing import Any, Callable

from pylage.ENGINE.components import Button, Form, Input, Row


def SearchBar(
    placeholder: Any = "Search...",
    button_text: Any = "Search",
    *,
    value: Any = None,
    on_change: Callable[[Any], Any] | None = None,
    on_search: Callable[[Any], Any] | None = None,
    class_name: str = "search-bar",
    **props: Any,
):
    """Create a reusable search bar using PyLage components."""
    input_props = {"placeholder": placeholder}
    if value is not None:
        input_props["value"] = value
    if on_change is not None:
        input_props["on_change"] = on_change

    btn_props = {}
    if on_search is not None:
        btn_props["on_click"] = on_search

    return Form(
        Row(
            Input(**input_props, class_name="search-input"),
            Button(button_text, **btn_props, class_name="search-button"),
            class_name="search-row",
        ),
        class_name=class_name,
        **props,
    )
