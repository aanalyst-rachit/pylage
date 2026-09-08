# PyLage UI Kit — Checkbox

## Definition

`checkbox()` is the public PyLage UI Kit wrapper for the existing engine `Checkbox` component.
It provides a simple checkbox API while reusing PyLage's existing rendering, registry, event, and State-reactivity infrastructure.

## Use

Use `checkbox()` for boolean input and interactive form controls.

- Basic unchecked or checked controls
- State-bound checked state
- Browser `change` events through `on_change`
- Disabled checkboxes
- Native checkbox properties such as `name`, `title`, and `class_name`
- Custom dimensions and styling through `Style`

## Usage

### Basic checkbox

```python
import pylage as pl

checkbox = pl.checkbox(
    name="terms",
    checked=False,
    title="Accept terms",
)
```

### Pre-checked checkbox

```python
import pylage as pl

checkbox = pl.checkbox(checked=True)
```

### State-bound checkbox

Pass a `pl.state` value to `checked` when the checkbox should participate in PyLage's reactive update system.

```python
import pylage as pl

checked = pl.state(False)

checkbox = pl.checkbox(
    checked=checked,
    on_change=lambda payload: checked.set(
        payload.get("checked", False)
        if isinstance(payload, dict)
        else bool(payload)
    ),
)
```

Changing the State updates the rendered/browser checkbox state, and the `on_change` handler can update the State from browser interaction.

### Custom change handler

`on_change` receives the existing engine event payload. A handler can read the `checked` value and perform application-specific updates.

```python
import pylage as pl

status = pl.state("Not changed yet")

def handle_change(payload):
    checked = payload.get("checked", False) if isinstance(payload, dict) else bool(payload)
    status.set(f"Checked: {checked}")

checkbox = pl.checkbox(
    checked=False,
    on_change=handle_change,
)
```

### Disabled checkbox

Use the forwarded `disabled` property when the control should not be interactive.

```python
import pylage as pl

checkbox = pl.checkbox(
    checked=True,
    disabled=True,
    title="Disabled checkbox",
)
```

### Custom styling

The wrapper provides default dimensions and cursor styling. A `Style` can override those values.

```python
import pylage as pl

checkbox = pl.checkbox(
    style=pl.style(
        width="1.25rem",
        height="1.25rem",
        cursor="pointer",
    )
)
```

## API

```python
checkbox(*, style=None, **props)
```

### Parameters

| Parameter | Description |
|---|---|
| `style` | Optional `Style` used to override or extend the wrapper's default checkbox styling. |
| `**props` | Additional properties forwarded directly to the existing engine `Checkbox`, including `checked`, `disabled`, `name`, `title`, `class_name`, and `on_change`. |

The `style` parameter is keyword-only.

## Styling Behavior

The UI Kit applies the following base style:

| Property | Default |
|---|---|
| `width` | `1rem` |
| `height` | `1rem` |
| `cursor` | `pointer` |

The final style is produced with:

```python
_BASE_STYLE.merge(style)
```

Therefore, values supplied through `style` take precedence over the corresponding defaults.

## Validation and Behavior

- The UI Kit wrapper does not introduce a separate checkbox renderer.
- `checked` is handled by the existing engine `Checkbox` and is registered as a boolean property.
- `checked=False` renders an unchecked checkbox.
- `checked=True` renders the checked state.
- A `State` supplied to `checked` is resolved for rendering and can update the browser checkbox reactively.
- `on_change` is forwarded to the engine event system.
- Additional component properties are forwarded through `**props`.

## API Boundary

The UI Kit layer is intentionally thin:

```text
pylage.UI.components.checkbox
        ↓
pylage.ENGINE.Checkbox
        ↓
PyLage registry / renderer / runtime
        ↓
Browser checkbox
```

No duplicate checkbox renderer, registry implementation, or runtime protocol is introduced by the UI Kit wrapper.

## Verified Working Examples

Primary manual example:

- `demo/demo_checkbox.py` — basic, State-bound, custom `on_change`, pre-checked, disabled, and styled checkbox cases.

Additional combined controls example:

- `demo/demo_slider_radio_checkbox.py` — checkbox used with State binding alongside other form controls.

## Verification

### Automated tests

Verified checkbox coverage includes:

- `test/browser/test_checkbox_api.py` — checked rendering, forwarded props/events, State resolution, registry metadata, and browser State synchronization.
- `test/components/test_checkbox.py` — checkbox rendering, forwarded properties, and checked behavior.

The browser tests verify the Python → State → WebSocket → browser DOM update path for `checked`.

## Verified Sources

- Component: `pylage/UI/components/checkbox.py`
- Demo: `demo/demo_checkbox.py`
- Combined demo: `demo/demo_slider_radio_checkbox.py`
- Engine tests: `test/components/test_checkbox.py`
- Browser/API tests: `test/browser/test_checkbox_api.py`

## Status

**FINAL / VERIFIED** — documentation reflects the current `checkbox()` implementation, verified demos, and available automated tests.
