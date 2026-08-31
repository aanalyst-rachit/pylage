from pyskin.app import run
from pyskin.components import (
    Accordion,
    Badge,
    Button,
    Card,
    Column,
    Grid,
    Heading,
    Input,
    Row,
    Text,
)
from pyskin.core.state import State

# --- 1. Global State Management ---
selected_component = State("Button")
custom_label = State("Click Me!")
button_variant = State("primary")

# Reactive dynamic code preview snippet generator
code_snippet = State(
    f'Button("{custom_label.value}", variant="{button_variant.value}")'
)


def update_label(new_val):
    custom_label.set(new_val)
    code_snippet.set(
        f'Button("{new_val}", variant="{button_variant.value}")'
    )


# --- 2. Left Panel: Code & Prompt Editor ---
code_editor_panel = Card(
    Heading("1. Prompt & Code Editor", level=2),
    Text("Select Component & Edit Props:"),
    Row(
        Button("Button", on_click=lambda: selected_component.set("Button")),
        Button("Input", on_click=lambda: selected_component.set("Input")),
        Button("Badge", on_click=lambda: selected_component.set("Badge")),
    ),
    Input(value=custom_label, on_change=update_label, placeholder="Change Button Text..."),
    Card(
        Heading("Generated PySkin Code:", level=3),
        Text(code_snippet),  # Bind directly to dynamic State
        style="background: #1e1e1e; color: #00ff00; padding: 12px; font-family: monospace; border-radius: 6px;",
    ),
    style="width: 50%; padding: 20px; border-right: 2px solid #e0e0e0;",
)

# --- 3. Right Panel: Visual Render & Component Showcase ---
visual_preview_panel = Card(
    Heading("2. Live Visual Render", level=2),
    Card(
        Heading("Live Output Window:", level=3),
        Button(value=custom_label, variant=button_variant.value),
        style="padding: 30px; border: 1px dashed #666; text-align: center; margin-bottom: 20px;",
    ),
    Heading("Library Component Inventory", level=3),
    Grid(
        Card(
            Heading("Inputs", level=4),
            Input(placeholder="Type here..."),
            Button("Submit"),
        ),
        Card(
            Heading("Badges & Tags", level=4),
            Badge("Active", color="green"),
            Badge("Pending", color="yellow"),
        ),
        columns=2,
    ),
    style="width: 50%; padding: 20px;",
)

# --- 4. Main Layout Assembly ---
showcase_app = Column(
    Heading("PySkin Interactive Showcase & Documentation", level=1),
    Row(code_editor_panel, visual_preview_panel),
    style="max-width: 1200px; margin: 0 auto; padding: 20px;",
)

if __name__ == "__main__":
    run(showcase_app, title="PySkin Playground", serve=True)