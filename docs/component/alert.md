# PyLage UI Kit — Alert

## Definition

`pl.alert()` provides a semantic feedback component for the PyLage UI Kit. It reuses the existing PyLage `Alert` component and renderer while adding semantic variants and UI Kit styling.

## Use

Use `pl.alert()` to present informational, success, warning, danger, or error feedback to users.

## Usage

### Basic Alert

```python
import pylage as pl

pl.alert("Your changes have been saved.")
```

### Variants

```python
import pylage as pl

pl.alert("Information available.", variant="default")
pl.alert("Profile updated successfully.", variant="success")
pl.alert("Please review the information.", variant="warning")
pl.alert("The operation failed.", variant="danger")
pl.alert("An unexpected error occurred.", variant="error")
pl.alert("Additional information.", variant="info")
```

Supported variants:

- `default` — neutral informational feedback
- `info` — informational feedback
- `success` — successful operation feedback
- `warning` — caution or review feedback
- `danger` — failure or destructive-operation feedback
- `error` — error feedback

The default variant is `default`.

### Component Composition

Existing PyLage components can be passed as children.

```python
import pylage as pl

pl.alert(
    pl.text("Alert with multiple children"),
    pl.text("Existing PyLage components remain valid children."),
    variant="info",
    title="Details",
)
```

Component children are preserved by the UI Kit wrapper.

Plain child values are normalized into existing PyLage `Text` components.

### Multiple Children

`pl.alert()` accepts any number of children. `None` children are ignored during normalization.

### Engine Properties

Existing PyLage Alert properties can be forwarded through `**props`.

```python
import pylage as pl

pl.alert(
    "Profile updated.",
    title="Notice",
    class_name="custom-alert",
)
```

## API

```python
alert(*children, variant="default", style=None, **props)
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*children` | `Any` | — | Alert content or existing PyLage components. |
| `variant` | `str` | `"default"` | Semantic visual variant. |
| `style` | `Style` | `None` | Custom style overrides. |
| `**props` | `Any` | — | Properties forwarded to the underlying PyLage Alert. |

## Validation

`variant` must be one of the supported semantic variants. An unknown value raises `ValueError`.

Valid variants are `default`, `info`, `success`, `warning`, `danger`, and `error`.

## Styling Behavior

The UI Kit builds the Alert style from a common base style and the selected semantic variant.

The final style is merged in this order:

1. UI Kit base style
2. Selected variant style
3. Explicit `style`, when supplied

Therefore, explicit custom styles take precedence over the UI Kit defaults.

The base style provides the Alert layout, spacing, gap, padding, and border radius. Variant styles provide semantic background, text, and border colors.

## API Boundary

`variant` is a UI Kit semantic property consumed by the wrapper and is not forwarded to the underlying engine component.

The implementation reuses the existing:

- `pylage.ENGINE.Alert`
- `PyLage Style`
- `pylage.ENGINE.Text`
- PyLage `Component`
- PyLage renderer

The UI Kit therefore provides a higher-level Alert API without introducing a second rendering or feedback system.

## Verified Working Example

The executable example is maintained in `demo/demo_alert.py`. It demonstrates all six semantic variants and an Alert composed from existing PyLage `Text` components.

## Verification

The implementation and tests verify:

- The UI Kit returns the existing PyLage `Alert` component type.
- Alert text is rendered correctly.
- All six semantic variants are supported.
- Unknown variants raise `ValueError`.
- `title` is forwarded to the underlying component.
- Other engine properties such as `class_name` are forwarded.
- Custom styles override the UI Kit defaults.
- Existing `Component` children are preserved.
- Plain child values are normalized to `Text` components.
- `None` children are ignored.

## Verified Sources

- Component source: `pylage/UI/components/alert.py`
- Demo: `demo/demo_alert.py`
- UI Kit tests: `test/components/test_ui_kit_alert.py`
- Engine tests: `test/components/test_alert.py`
- Reference documentation: `documents/alert.md`

## Status

**Verified against the current Alert implementation, demo, and test coverage.**
