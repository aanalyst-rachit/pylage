from __future__ import annotations

from typing import Any

from pylage.ENGINE.core.component import Component, component
from pylage.ENGINE.core.state import State


def Text(text: Any, **props: Any) -> Component:
    return component("Text", text=text, **props)


def Label(text: Any, **props: Any) -> Component:
    return component("Label", text=text, **props)


def Column(*children, **props: Any) -> Component:
    return component("Column", *children, **props)


def Row(*children, **props: Any) -> Component:
    return component("Row", *children, **props)


def Card(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Card",
        "div",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Card", *children, **props)



def Divider(*children, **props: Any) -> Component:
    return component("Divider", *children, **props)

def Badge(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Badge",
        "span",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Badge", *children, **props)


def Avatar(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Avatar",
        "span",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Avatar", *children, **props)


def Accordion(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Accordion",
        "div",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
            "value": PropDefinition(
                "value",
                kind="attribute",
                html_name="value",
            ),
        },
    )

    return component("Accordion", *children, **props)


def Carousel(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Carousel",
        "div",
        props={
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
            "value": PropDefinition(
                "value",
                kind="attribute",
                html_name="value",
            ),
        },
    )

    return component("Carousel", *children, **props)


def Grid(*children, **props: Any) -> Component:
    return component("Grid", *children, **props)


def Image(**props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Image",
        "img",
        void=True,
        props={
            "src": PropDefinition(
                "src",
                kind="attribute",
                html_name="src",
            ),
            "alt": PropDefinition(
                "alt",
                kind="attribute",
                html_name="alt",
            ),
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Image", **props)


def Video(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Video",
        "video",
        props={
            "src": PropDefinition(
                "src",
                kind="attribute",
                html_name="src",
            ),
            "controls": PropDefinition(
                "controls",
                kind="boolean",
                html_name="controls",
            ),
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Video", *children, **props)


def Audio(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Audio",
        "audio",
        props={
            "src": PropDefinition(
                "src",
                kind="attribute",
                html_name="src",
            ),
            "controls": PropDefinition(
                "controls",
                kind="boolean",
                html_name="controls",
            ),
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Audio", *children, **props)


def Icon(**props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Icon",
        "span",
        props={
            "name": PropDefinition(
                "name",
                kind="text",
            ),
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Icon", **props)


def Canvas(*children, **props: Any) -> Component:
    from pylage.ENGINE.core.registry import PropDefinition, registry

    registry.register_if_missing(
        "Canvas",
        "svg",
        props={
            "width": PropDefinition(
                "width",
                kind="attribute",
                html_name="width",
            ),
            "height": PropDefinition(
                "height",
                kind="attribute",
                html_name="height",
            ),
            "class_name": PropDefinition(
                "class_name",
                kind="attribute",
                html_name="class",
            ),
            "title": PropDefinition(
                "title",
                kind="attribute",
                html_name="title",
            ),
        },
    )

    return component("Canvas", *children, **props)


def Heading(text: Any, **props: Any) -> Component:
    return component("Heading", text=text, **props)


def Button(text: Any, **props: Any) -> Component:
    return component("Button", text=text, **props)


def Input(
    value: Any = "",
    input_type: str | None = None,
    **props: Any,
) -> Component:
    if input_type is not None:
        props["_html_type"] = input_type

    if isinstance(value, State) and "on_input" not in props:
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

        props["on_input"] = update_state

    return component("Input", value=value, **props)


def Form(*children, **props: Any) -> Component:
    return component("Form", *children, **props)


def Table(*children, data: Any = None, headers: Any = None, **props: Any) -> Component:
    if data is None and len(children) == 1 and not isinstance(children[0], Component):
        candidate = children[0]
        if isinstance(candidate, (dict, list, tuple)) or hasattr(candidate, "columns"):
            data = candidate
            children = ()
    if data is not None:
        props["data"] = data
    if headers is not None:
        props["headers"] = headers
    return component("Table", *children, **props)


def DataFrame(
    *children,
    data: Any = None,
    headers: Any = None,
    **props: Any,
) -> Component:
    if data is None and len(children) == 1 and not isinstance(children[0], Component):
        candidate = children[0]
        if isinstance(candidate, (dict, list, tuple)) or hasattr(candidate, "columns"):
            data = candidate
            children = ()

    if data is not None:
        props["data"] = data

    if headers is not None:
        props["headers"] = headers

    return component("DataFrame", *children, **props)


def Dialog(*children, **props: Any) -> Component:
    return component("Dialog", *children, **props)


def Navigation(*children, **props: Any) -> Component:
    return component("Navigation", *children, **props)


def Tabs(*children, **props: Any) -> Component:
    return component("Tabs", *children, **props)


def Checkbox(**props: Any) -> Component:
    checked = props.get("checked")
    user_on_change = props.get("on_change")

    checkbox = component("Checkbox", **props)

    if isinstance(checked, State):
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "checked" in payload:
                checked.set(bool(payload["checked"]))

            if user_on_change is not None:
                user_on_change(payload)

        checkbox.events["change"] = update_state

    return checkbox


def RadioGroup(*children, **props: Any) -> Component:
    value = props.pop("value", None)
    user_on_change = props.pop("on_change", None)

    group = component("RadioGroup", *children, **props)

    checked_states: list[tuple[Component, State]] = []

    for child in group.children:
        if not isinstance(child, Component):
            continue

        if child.type != "Input":
            continue

        if child.props.get("_html_type") != "radio":
            continue

        initial_checked = bool(child.props.get("checked", False))

        checked_state = State(initial_checked)

        child.props["checked"] = checked_state
        checked_states.append((child, checked_state))

    def sync_selected(selected: Any) -> None:
        for child, checked_state in checked_states:
            checked_state.set(
                child.props.get("value") == selected
            )

    if value is not None:
        selected = (
            value.value
            if isinstance(value, State)
            else value
        )

        sync_selected(selected)

    def update_state(payload: Any) -> None:
        if isinstance(payload, dict):
            selected = payload.get("value")

            if selected is not None:
                if isinstance(value, State):
                    value.set(selected)

                sync_selected(selected)

        if user_on_change is not None:
            user_on_change(payload)

    if value is not None or user_on_change is not None:
        group.events["change"] = update_state

    if isinstance(value, State):
        value.subscribe(
            lambda _old, new: sync_selected(new)
        )

    return group

def Switch(**props: Any) -> Component:
    checked = props.get("checked")
    user_on_change = props.get("on_change")

    switch = component("Switch", **props)

    if isinstance(checked, State):
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "checked" in payload:
                checked.set(bool(payload["checked"]))

            if user_on_change is not None:
                user_on_change(payload)

        switch.events["change"] = update_state

        checked.subscribe(
            lambda _old, new: switch.props.__setitem__("checked", bool(new))
        )

    return switch


def Select(*children, **props: Any) -> Component:
    value = props.get("value")
    user_on_change = props.get("on_change")

    select = component("Select", *children, **props)

    if isinstance(value, State):
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

            if user_on_change is not None:
                user_on_change(payload)

        select.events["change"] = update_state

    return select


def Option(text: Any, value: Any = None, **props: Any) -> Component:
    if value is not None:
        props["value"] = value

    return component("Option", text=text, **props)


def Slider(**props: Any) -> Component:
    value = props.get("value")
    user_on_input = props.get("on_input")

    slider = component("Slider", **props)

    if isinstance(value, State):
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

            if user_on_input is not None:
                user_on_input(payload)

        slider.events["input"] = update_state

    return slider


def DatePicker(**props: Any) -> Component:
    value = props.get("value")
    user_on_input = props.get("on_input")

    datepicker = component("DatePicker", **props)

    if isinstance(value, State):
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

            if user_on_input is not None:
                user_on_input(payload)

        datepicker.events["input"] = update_state

    return datepicker


def Alert(*children, **props: Any) -> Component:
    return component("Alert", *children, **props)


def Toast(*children, **props: Any) -> Component:
    return component("Toast", *children, **props)


def Spinner(*children, **props: Any) -> Component:
    return component("Spinner", *children, **props)


def ProgressBar(*children, **props: Any) -> Component:
    return component("ProgressBar", *children, **props)


def Skeleton(*children, **props: Any) -> Component:
    return component("Skeleton", *children, **props)


def Breadcrumbs(*children, **props: Any) -> Component:
    return component("Breadcrumbs", *children, **props)


def Pagination(*children, **props: Any) -> Component:
    return component("Pagination", *children, **props)


def Menu(*children, **props: Any) -> Component:
    return component("Menu", *children, **props)


def Drawer(*children, **props: Any) -> Component:
    return component("Drawer", *children, **props)


def Tooltip(*children, **props: Any) -> Component:
    return component("Tooltip", *children, **props)


def Popover(*children, **props: Any) -> Component:
    return component("Popover", *children, **props)
