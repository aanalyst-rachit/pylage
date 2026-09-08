# PyLage UI Kit — Error State

## Definition

`error_state()` is a semantic, high-level UI Kit component for presenting page, section, operation, or system-level error feedback. It composes an optional icon, title, description, and recovery action inside a styled PyLage `Column`.

It is intended for broader error states rather than field-level validation feedback. Field-specific errors can instead be presented through the form components that support validation.

## Use

Use `error_state()` when an operation or view cannot provide its expected content and the user needs an explanation or possible recovery action.

Common uses include:

- Failed data loading
- Expired authentication sessions
- Invalid file or input formats
- Remote service failures
- Other page or section-level failures

## Usage

### Basic error state

```python
import pylage as pl

pl.error_state()
```

The default state includes a warning icon, error title, and explanatory description.

### Custom error state

```python
import pylage as pl

pl.error_state(
    title="Failed to load dashboard",
    description="The network connection timed out.",
    icon="❌",
)
```

### With a recovery action

An existing PyLage component can be supplied as the `action`.

```python
import pylage as pl

pl.error_state(
    title="Server unreachable",
    description="The remote service could not be reached.",
    action=pl.button("Retry request", variant="danger"),
)
```

### In a layout

`error_state()` can be composed with normal PyLage layout components.

```python
import pylage as pl

pl.grid(
    pl.error_state(
        title="Failed to fetch data",
        description="The remote server returned an error.",
        icon="⚠️",
        action=pl.button("Retry connection", variant="danger"),
    ),
    pl.error_state(
        title="Authentication required",
        description="Please sign in again to continue.",
        icon="🔒",
        action=pl.button("Sign In", variant="primary"),
    ),
)
```

## API

```python
error_state(
    title="Something went wrong",
    description="An error occurred while processing your request.",
    *,
    icon="⚠️",
    action=None,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `Any` | `"Something went wrong"` | Primary error heading. |
| `description` | `Any` | `"An error occurred while processing your request."` | Error explanation or recovery guidance. |
| `icon` | `Any` | `"⚠️"` | Optional icon content. Strings receive the built-in icon-container styling; other values are inserted as content. |
| `action` | `Any` | `None` | Optional recovery or action component. |
| `style` | `Style` | `None` | Optional style merged with the default container style. |
| `**props` | `Any` | — | Additional properties forwarded to the root `Column`. |

## Content Behavior

The component builds its contents in this order:

1. `icon`, when supplied
2. `title`, when not `None`
3. `description`, when not `None`
4. `action`, when supplied

The `icon` can be disabled by passing `None`. The `title` and `description` can also be omitted by passing `None`.

## Default Styling

The root container uses:

- `display: flex`
- `flex-direction: column`
- `align-items: center`
- `justify-content: center`
- `text-align: center`
- `padding: var(--spacing-2xl)`
- `background-color: var(--color-background)`
- `border: 1px solid var(--color-danger-border)`
- `border-radius: var(--radius-xl)`
- `gap: var(--spacing-sm)`

The title uses the danger color, the description uses the muted text color, and a string icon receives a dedicated danger-themed icon container.

## Styling Behavior

The optional `style` is merged with the default container style:

```python
final_style = _DEFAULT_CONTAINER_STYLE.merge(style)
```

Explicit style values override matching defaults while unspecified defaults remain active.

For example:

```python
import pylage as pl

pl.error_state(
    title="Service unavailable",
    style=pl.style(
        padding="3.5rem",
        background_color="#fff5f5",
    ),
)
```

## Composition

`error_state()` returns a PyLage `Column` containing the generated error-state content. Existing PyLage components can be supplied as the action or as non-string icon content.

## API Boundary

The UI Kit component owns the error-state structure and default styling. Additional `**props` are forwarded to the root `Column`, allowing engine-supported properties such as `class_name` and `id` to be used.

## Verified Working Example

The project demo `demo/demo_error_state.py` renders three error-state variants in a responsive grid: a failed data request with retry action, an authentication error with a sign-in action, and an invalid file-format error without an action.

## Verification

Verified coverage includes:

- Returns a PyLage `Column`
- Default title, description, and warning icon
- Custom title, description, and icon
- Action component rendering
- Custom style overrides
- Engine property forwarding through `class_name` and `id`

## Verified Sources

- `pylage/UI/components/error_state.py`
- `demo/demo_error_state.py`
- `test/components/test_ui_kit_error_state.py`
- `documents/error_state.md` (reference/archive)

## Status

Error State documentation is refined against the current implementation, demo, and verified tests.
