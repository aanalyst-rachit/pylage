# PyLage UI Kit — Form Field

## Definition

`form_field` is a semantic composition helper for wrapping an existing PyLage UI control with field-level presentation.

It combines a control with an optional label, help text, error message, and required-field presentation without introducing a separate renderer or input implementation.

## Use

Use `form_field()` when a form control needs consistent field-level structure and accessibility metadata.

It is designed to work with existing controls such as `input()`, `textarea()`, and `select()`.

## Usage

### Basic Field

```python
import pylage as pl

pl.form_field(
    pl.input(value="user@example.com"),
    label="Email",
)
```

### Help and Error Text

```python
pl.form_field(
    pl.input(name="email"),
    label="Email",
    help_text="Use your work email.",
    error="Email is required.",
)
```

### Required Field

```python
pl.form_field(
    pl.input(name="email"),
    label="Email",
    required=True,
)
```

When `required=True`, the wrapped control receives `required=True` and the label is displayed with a required marker.

### Different Controls

```python
pl.form_field(
    pl.textarea(name="message"),
    label="Message",
)

pl.form_field(
    pl.select(
        pl.option("India", value="IN"),
        pl.option("United States", value="US"),
        name="country",
    ),
    label="Country",
)
```

## API

```python
form_field(
    child,
    label=None,
    help_text=None,
    error=None,
    required=False,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `child` | Existing PyLage UI control wrapped by the field. |
| `label` | Optional label displayed for the control. |
| `help_text` | Optional supporting text displayed below the control. |
| `error` | Optional error message displayed below the control. |
| `required` | When `True`, marks the control as required and adds a required marker to the label. |
| `style` | Optional style applied to the field container. |
| `**props` | Additional properties forwarded to the underlying `Stack` container. |

## Composition Behavior

The field is composed in this order when the corresponding values are provided:

1. Label
2. Wrapped control
3. Help text
4. Error text

The wrapped control remains the original PyLage component and keeps its existing behavior.

## Label and Control Association

When a label is provided, `form_field()` ensures the control has an `id` and creates a label associated with that control through the HTML `for` relationship.

If the control already has an `id`, that identifier is preserved. Otherwise, a PyLage field identifier is generated.

## Accessibility Behavior

`form_field()` adds accessibility relationships for supporting and error text.

- Existing `aria-describedby` references are preserved.
- Help text receives a generated identifier and is added to `aria-describedby`.
- Error text receives a generated identifier and is added to `aria-describedby`.
- Duplicate `aria-describedby` identifiers are removed while preserving their order.
- When `error` is provided, the control receives `aria-invalid="true"`.

When `required=True`, the control also receives the native `required` property unless it was already explicitly provided.

## Help and Error Presentation

`help_text` provides supporting information for the field.

`error` provides field-level error presentation. FormField presents the supplied error value but does not perform validation itself; validation logic remains outside this composition helper.

## State and Events

FormField preserves the wrapped control rather than replacing it with a new input implementation.

State binding and control-specific events therefore remain the responsibility of the wrapped control.

## Styling

`form_field()` does not define a separate component-level default style. The optional `style` argument is passed to the underlying `Stack` container.

This allows the field container to participate naturally in the existing PyLage layout and styling system.

## Architecture

FormField is intentionally a composition component:

```text
form_field()
   ↓
Label + existing control + optional text
   ↓
Stack
   ↓
Existing PyLage renderer + runtime
```

It does not introduce a duplicate renderer, reactive engine, or input implementation.

## API Boundary

FormField owns field-level composition and accessibility relationships.

The wrapped control owns its own value, state binding, and control-specific event behavior.

Form-level submission and composition belong to `form()` rather than `form_field()`.

## Verified Working Example

The project demo is `demo/demo_form_field.py`.

It demonstrates FormField with Input, Textarea, and Select controls, including labels, required fields, help text, error presentation, and state-bound examples.

## Verification

The implementation is covered by:

- `test/components/test_form_field.py`
- `test/browser/test_form_field.py`

The tests verify field composition, label and required behavior, help and error presentation, accessibility attributes, supported controls, and browser interaction.

## Verified Sources

- `pylage/UI/components/form_field.py`
- `demo/demo_form_field.py`
- `test/components/test_form_field.py`
- `test/browser/test_form_field.py`
- `documents/form_field.md`

## Status

**Form Field documentation refined and verified.**
