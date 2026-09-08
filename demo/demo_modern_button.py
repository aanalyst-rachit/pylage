import pylage as pl
from pathlib import Path
from pylage.ENGINE.core.component import component


def Option(label: str, value: str, **props):
    """Helper component for pl.select dropdown options."""
    return component("option", label, value=value, **props)


def RadioInput(name: str, value: str, checked: bool = False, on_change=None):
    """Helper component to avoid keyword collision on 'type' argument."""
    return component(
        "input",
        name=name,
        value=value,
        checked=checked,
        on_change=on_change,
        props={"type": "radio"},
    )


def get_app():
    # -------------------------------------------------------------
    # REACTIVE STATES
    # -------------------------------------------------------------
    selected_theme = pl.state("Dark Mode")
    switch_active = pl.state(True)
    selected_framework = pl.state("PyLage")

    # -------------------------------------------------------------
    # EVENT HANDLERS
    # -------------------------------------------------------------
    def on_radio_change(payload=None):
        if isinstance(payload, dict) and "value" in payload:
            selected_theme.set(payload["value"])
        elif isinstance(payload, str):
            selected_theme.set(payload)

    def on_switch_toggle(payload=None):
        if isinstance(payload, dict) and "checked" in payload:
            switch_active.set(payload["checked"])
        else:
            switch_active.set(not switch_active.get())

    def on_select_change(payload=None):
        if isinstance(payload, dict) and "value" in payload:
            selected_framework.set(payload["value"])
        elif isinstance(payload, str):
            selected_framework.set(payload)

    # -------------------------------------------------------------
    # UI COMPONENTS LAYOUT
    # -------------------------------------------------------------
    return pl.column(
        pl.heading("PyLage Components Working Live Demo"),
        # 1. RADIO BUTTON GROUP DEMO
        pl.card(
            pl.heading("1. Radio Group Component"),
            pl.radio_group(
                pl.row(
                    RadioInput(
                        name="theme_group",
                        value="Light Mode",
                        on_change=on_radio_change,
                    ),
                    pl.text("Light Mode"),
                ),
                pl.row(
                    RadioInput(
                        name="theme_group",
                        value="Dark Mode",
                        checked=True,
                        on_change=on_radio_change,
                    ),
                    pl.text("Dark Mode"),
                ),
                pl.row(
                    RadioInput(
                        name="theme_group",
                        value="System Default",
                        on_change=on_radio_change,
                    ),
                    pl.text("System Default"),
                ),
            ),
            pl.text("Selected Theme: "),
            pl.text(selected_theme),
            class_name="demo-card",
        ),
        # 2. SWITCH COMPONENT DEMO
        pl.card(
            pl.heading("2. pl.switch Component"),
            pl.row(
                pl.switch(
                    checked=switch_active,
                    on_change=on_switch_toggle,
                    title="Toggle Status",
                ),
                pl.text("Toggle pl.switch pl.State"),
            ),
            pl.text("pl.switch Active Status: "),
            pl.text(switch_active),
            class_name="demo-card",
        ),
        # 3. SELECT COMPONENT DEMO
        pl.card(
            pl.heading("3. pl.select Component"),
            pl.select(
                Option("PyLage UI Framework", "PyLage"),
                Option("React Web Engine", "React"),
                Option("VueJS Framework", "Vue"),
                value=selected_framework,
                on_change=on_select_change,
            ),
            pl.text("Selected Option: "),
            pl.text(selected_framework),
            class_name="demo-card",
        ),
        class_name="container",
    )
