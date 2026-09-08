# PyLage UI Kit — Disabled State

## Definition

Disabled state is a control-level property exposed through the existing PyLage component and renderer infrastructure. The UI Kit does not introduce a separate disabled-state component or rendering system.

The public UI controls accept `disabled` through their existing component property forwarding where the underlying control supports it.

## Use

Use `disabled=True` when a control should be unavailable for user interaction while remaining part of the rendered interface.

```python
import pylage as pl

pl.input(disabled=True)
pl.button("Save", disabled=True)
pl.textarea(disabled=True)
```

The property is forwarded to the underlying control and rendered using the existing PyLage property and HTML handling.

## Supported Public Controls

The current UI Kit public control API includes these controls that can receive control properties through the existing `**props` boundary:

- `input()`
- `select()`
- `checkbox()`
- `radio_group()`
- `switch()`
- `slider()`
- `datepicker()`
- `textarea()`
- `button()`

The repository has direct disabled rendering assertions for Input, Textarea, and the UI Kit Button wrapper. The other controls reuse the existing property-forwarding boundary; this document does not claim separate disabled-specific tests for each control.

## Boolean Property Contract

Disabled state is represented as a boolean HTML property where the underlying component defines the corresponding control contract.

For example, the Engine Textarea registry explicitly defines `disabled` as a boolean property mapped to the HTML `disabled` attribute:

```text
Textarea → disabled → boolean HTML property → renderer
```

The UI Kit Textarea wrapper delegates rendering to the existing Engine component rather than implementing a second disabled-state path.

## Reactive Disabled State

The existing PyLage reactive property system supports `disabled` as a reactive property. A `State` value can be attached to a component property and updated through the established runtime.

```python
import pylage as pl

disabled = pl.state(False)
button = pl.button("Save", disabled=disabled)

disabled.set(True)
disabled.set(False)
```

Reactive property updates are handled by the existing PyLage runtime. The client runtime uses generic reactive-property handling rather than a hard-coded `disabled` dispatch branch.

## Accessibility Behavior

Disabled controls participate in the existing browser accessibility behavior. Browser regression coverage verifies that disabled form controls are skipped during keyboard focus navigation.

The accessibility tests specifically verify that a disabled input and disabled button are not selected by keyboard focus while enabled controls remain focusable.

Disabled state therefore relies on native control semantics rather than a UI Kit-specific keyboard-navigation implementation.

## Architecture

```text
UI Kit control
      ↓
existing component property boundary
      ↓
PyLage Engine component / registry
      ↓
existing renderer and reactive runtime
      ↓
browser disabled semantics
```

No duplicate disabled-state abstraction, renderer, scheduler, WebSocket mechanism, or client-side dispatch implementation is introduced by the UI Kit.

## Verification

Focused regression verification completed with:

- `test/components/test_ui_kit_button.py`
- `test/components/test_input_type_api.py`
- `test/components/test_textarea.py`
- `test/browser/test_accessibility_keyboard.py`
- `test/browser/test_generic_reactive_props.py`

Result: **45 passed in 6.60s**.

The verification covers disabled property forwarding and rendering, the Textarea boolean property contract, keyboard-focus accessibility behavior, and generic reactive-property handling.

No dedicated `ui_kit_*_manual.py` disabled-state manual was found in the current `demo/` directory. Disabled behavior is therefore documented from the current component contracts and automated/browser regression coverage rather than from a dedicated manual application.

## Verified Sources

- UI Kit controls: `pylage/UI/components/button.py`, `input.py`, `select.py`, `checkbox.py`, `radio.py`, `switch.py`, `slider.py`, `datepicker.py`, `textarea.py`
- Engine property contract: `pylage/ENGINE/core/registry.py`
- UI Kit exports: `pylage/UI/__init__.py` and `pylage/UI/components/__init__.py`
- Component tests: `test/components/test_ui_kit_button.py`, `test/components/test_input_type_api.py`, `test/components/test_textarea.py`
- Browser tests: `test/browser/test_accessibility_keyboard.py`, `test/browser/test_generic_reactive_props.py`, `test/browser/test_reactive_props.py`

## Status

**FINAL / VERIFIED** — documentation reflects the current disabled-property forwarding, native browser semantics, reactive property infrastructure, and verified automated/browser coverage.