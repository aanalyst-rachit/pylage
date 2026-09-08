# UI Kit Help Text

## Overview

Help text is supporting information presented through the existing `form_field()` composition component.

Help Text is not a standalone component or renderer. It is composed with an existing form control by passing the `help_text` argument to `form_field()`.

## Usage

```python
import pylage as pl

pl.form_field(
    pl.input(placeholder="Email address"),
    label="Email",
    help_text="Use your work email address.",
)
```

The wrapped control remains the actual input control; `form_field()` adds the supporting help content around it.

## Presentation

When `help_text` is provided, `form_field()` creates an existing PyLage `Text` component after the wrapped control.

The generated help text uses the existing text presentation metadata:

- `muted=True`
- `caption=True`
- A generated field-specific `id`

The generated ID follows the form field help-text pattern `pylage-field-help-*`.

## Accessibility

Help text is associated with the wrapped control through `aria-describedby`.

For example, the control receives an `aria-describedby` value containing the generated help-text ID:

```html
aria-describedby="pylage-field-help-..."
```

If the control already has an `aria-describedby` value, `form_field()` preserves the existing references and adds the generated help-text reference.

## Composition

```text
form_field()
├── Optional Label
├── Existing control
└── Optional Help Text
```

Help text can therefore be used with the existing controls supported by `form_field()`, including Input, Textarea, and Select.

## Relationship to Validation

Help text provides supporting information and is separate from validation error presentation.

Use `help_text` for instructional or contextual information. Use the `error` argument when presenting a field-level validation error.

`form_field()` presents the supplied content but does not perform validation itself.

## Verification

Help Text is covered by the existing FormField verification:

- `test/components/test_form_field.py` verifies help-text rendering and accessibility metadata.
- `test/browser/test_form_field.py` verifies help text in the browser and its accessibility relationship.
- `demo/demo_form_field.py` provides manual Help Text examples with Textarea, Input, and Select controls.

## Source

The implementation is provided by `pylage/UI/components/form_field.py` through the `help_text` parameter of `form_field()`.
