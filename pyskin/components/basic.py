from __future__ import annotations

from typing import Any

from pyskin.core.component import Component, component
from pyskin.core.state import State


def Column(*children, **props: Any) -> Component:
    return component("Column", *children, **props)


def Heading(text: Any, **props: Any) -> Component:
    return component("Heading", text=text, **props)


def Button(text: Any, **props: Any) -> Component:
    return component("Button", text=text, **props)


def Input(value: Any = "", **props: Any) -> Component:
    if isinstance(value, State) and "on_input" not in props:
        def update_state(payload: Any) -> None:
            if isinstance(payload, dict) and "value" in payload:
                value.set(payload["value"])

        props["on_input"] = update_state

    return component("Input", value=value, **props)
