# PyLage UI Kit — Toast

## Definition

`toast` is a PyLage UI Kit component for transient feedback messages.

It is a thin wrapper around the existing PyLage engine `Toast`, adding semantic variants, UI Kit styling, and child normalization.

## Use

Use `toast()` to present short informational, success, warning, or error feedback to the user.

## Usage

### Basic Toast

```python
import pylage as pl

pl.toast("Profile saved.")
```

### Semantic Variants

The `variant` argument selects the semantic presentation:

- `default` — neutral feedback.
- `info` — informational feedback.
- `success` — successful operation feedback.
- `warning` — warning feedback.
- `danger` — danger or destructive feedback.
- `error` — error feedback.

```python
import pylage as pl

pl.toast("Changes saved.", variant="success")
pl.toast("Check your settings.", variant="warning")
pl.toast("Something went wrong.", variant="error")
```

### Component Children

Toast accepts existing PyLage components as children.

```python
import pylage as pl

pl.toast(
    pl.text("Your changes are ready."),
    variant="info",
)
```

Plain child values are automatically normalized into existing PyLage `Text` components. Existing `Component` instances are preserved.

### Multiple Children

Multiple children can be supplied when a toast needs more than one piece of content:

```python
import pylage as pl

pl.toast(
    pl.text("Upload complete"),
    pl.text("3 files were processed."),
    variant="success",
)
```

### Visibility

The underlying engine `Toast` supports the existing `visible` property.

```python
import pylage as pl

pl.toast("Saved.", visible=True)
```

Visibility is handled through the existing PyLage rendering system rather than a Toast-specific state mechanism.

## API

```python
toast(*children, variant="default", style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `*children` | `Any` | — | Toast content. Existing components are preserved; other non-`None` values are converted to `Text`. |
| `variant` | `str` | `"default"` | Semantic toast variant. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit defaults and selected variant styles. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Toast`. |

## Variants

Supported variants are:

| Variant | Background | Text | Border |
| --- | --- | --- | --- |
| `default` | `var(--color-surface-variant)` | `var(--color-text)` | `var(--color-border)` |
| `info` | `var(--color-info)` | `var(--color-primary-contrast)` | `var(--color-info)` |
| `success` | `var(--color-success)` | `var(--color-primary-contrast)` | `var(--color-success)` |
| `warning` | `var(--color-warning)` | `var(--color-text)` | `var(--color-warning)` |
| `danger` | `var(--color-danger)` | `var(--color-primary-contrast)` | `var(--color-danger)` |
| `error` | `var(--color-danger)` | `var(--color-primary-contrast)` | `var(--color-danger)` |

`danger` and `error` currently use the same semantic color styling.

An unsupported variant raises `ValueError` and reports the valid variant names.

## Default Styling

The UI Kit applies these base styles to every toast:

- `display: flex`
- `flex_direction: column`
- `gap: var(--spacing-xs)`
- `padding: var(--spacing-md)`
- `border_radius: var(--radius-md)`

The selected variant then supplies its semantic background, text, and border styles.

## Styling Behavior

Styles are merged in this order:

1. Base Toast UI Kit styles.
2. Selected variant styles.
3. User-supplied `style`.

Therefore, a supplied `Style` value takes precedence over both the base and variant defaults.

```python
import pylage as pl

pl.toast(
    "Custom toast",
    variant="info",
    style=pl.style(
        padding="1rem",
        border_radius="0.5rem",
    ),
)
```

## Visibility and Rendering

Toast visibility uses the existing engine `visible` behavior.

The PyLage renderer preserves the native hidden state with the framework `[hidden]` CSS rule, so hidden Toast components remain hidden even when their inline styling includes a display value.

The UI Kit wrapper does not add Toast-specific JavaScript for visibility.

## State and Events

The UI Kit Toast does not introduce a separate state or event system. Existing engine properties and runtime behavior are forwarded through `**props`.

Application-level visibility, toggling, and event handling can therefore use the existing PyLage component and state APIs.

## Architecture

```text
pl.toast()
    ↓
UI Kit toast wrapper
    ↓
PyLage ENGINE Toast
    ↓
Existing renderer / reactive runtime
```

The wrapper owns semantic variants, UI Kit styles, and child normalization. Rendering and runtime behavior remain owned by the existing PyLage engine.

## API Boundary

`toast()` is the public UI Kit entry point.

It returns the existing engine `Toast` component and does not introduce a separate renderer, notification system, or state engine.

## Verified Working Example

The project provides the executable Toast demo:

- `demo/demo_toast.py`

The demo exercises Toast creation, semantic variants, visibility, and UI interaction.

## Verification

Toast behavior is covered by:

- `test/components/test_toast.py`
- `test/components/test_ui_kit_toast.py`

The verification coverage includes Toast behavior, UI Kit wrapper behavior, semantic variants, styling, and visibility rendering.

## Verified Sources

- `pylage/UI/components/toast.py`
- `demo/demo_toast.py`
- `test/components/test_toast.py`
- `test/components/test_ui_kit_toast.py`
- `documents/toast.md`

## Status

**Toast documentation refined and verified.**
