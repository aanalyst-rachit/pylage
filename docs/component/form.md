# PyLage UI Kit — Form

## Definition

`form` is the public PyLage UI Kit wrapper around the existing engine `Form` component.

It provides semantic HTML form composition, native form attributes, and submit-event integration while reusing the existing PyLage renderer and client runtime.

## Use

Use `form()` to group controls into a semantic form and handle submitted values through `on_submit`.

Typical form content can include `form_field()`, `input()`, `textarea()`, `select()`, `checkbox()`, and submit buttons.

## Usage

### Basic Form

```python
import pylage as pl

def handle_submit(payload):
    print(payload)

pl.form(
    pl.form_field(
        pl.input(name="email"),
        label="Email",
        required=True,
    ),
    pl.button("Submit", type="submit"),
    on_submit=handle_submit,
)
```

### Native Form Attributes

Native form properties such as `method` and `action` can be passed through to the rendered form.

```python
pl.form(
    pl.input(name="email"),
    method="post",
    action="/submit",
)
```

### Composed Controls

Forms accept normal PyLage children, so controls can be combined with layout and field components as needed.

```python
pl.form(
    pl.form_field(
        pl.input(name="name"),
        label="Name",
    ),
    pl.form_field(
        pl.input(name="email"),
        label="Email",
    ),
    pl.button("Submit", type="submit"),
)
```

## API

```python
form(*children, style=None, **props)
```

### Parameters

| Parameter | Description |
| --- | --- |
| `*children` | Child PyLage components rendered inside the form. |
| `style` | Optional `Style` merged with the component default style. |
| `**props` | Additional properties forwarded to the underlying engine `Form`. |

## Default Styling

The public wrapper applies this base layout style:

- `display: flex`
- `flex-direction: column`
- `gap: 1rem`
- `width: 100%`

The supplied `style` is merged with these defaults, allowing individual properties to be overridden.

## Submit Events

`on_submit` integrates with the existing PyLage client event runtime.

When a form is submitted, the browser-side form handler prevents native page navigation, collects submitted controls through `FormData`, and sends the values through the existing PyLage event protocol.

The verified payload structure is:

```python
{
    "values": {
        "email": "user@example.com",
    }
}
```

## Form and FormField

`form()` and `form_field()` have separate responsibilities.

`form()` provides form-level composition and submission behavior.

`form_field()` provides field-level presentation around an individual control, including its label, help text, and error presentation.

Typical composition is:

```text
Form
├── FormField
│   ├── Label
│   ├── Control
│   ├── Help text
│   └── Error
├── Other controls
└── Submit action
```

## Architecture

The public wrapper reuses the existing engine implementation:

```text
pl.form()
   ↓
UI Kit form wrapper
   ↓
ENGINE Form
   ↓
Component("Form")
   ↓
Existing renderer + client runtime
```

No duplicate renderer, WebSocket layer, reactive engine, or separate form implementation is introduced by the UI Kit wrapper.

## API Boundary

The UI Kit owns the public `form()` entry point and its default styling.

Form rendering, native form behavior, and client-side submit handling remain part of the existing engine and runtime.

## Verified Working Example

The project demo is `demo/demo_form.py`.

It demonstrates a composed form using form fields, inputs, checkbox controls, styling, state, and a submit handler.

## Verification

The implementation is covered by the following verified tests:

- `test/browser/test_form.py`
- `test/browser/test_form_control_visual_foundation.py`
- `test/browser/test_form_field.py`
- `test/components/test_form_field.py`
- `test/integration/test_form_component.py`

Browser and integration coverage verifies form rendering, control interaction, and submit behavior.

## Verified Sources

- `pylage/UI/components/form.py`
- `demo/demo_form.py`
- `demo/demo_form_field.py`
- `test/browser/test_form.py`
- `test/browser/test_form_control_visual_foundation.py`
- `test/browser/test_form_field.py`
- `test/components/test_form_field.py`
- `test/integration/test_form_component.py`
- `documents/form.md`

## Status

**Form documentation refined and verified.**
