# PyLage UI Kit — Loading State

## Definition

`loading_state` is a reusable PyLage UI Kit component for presenting a semantic loading indicator during data fetching, processing, synchronization, and other asynchronous workflows.

It composes an existing `Column` with an optional `Spinner`, primary loading text, and optional descriptive text.

## Use

Use `loading_state()` when the application needs an inline or page-level visual indication that work is in progress without requiring a blocking full-viewport overlay.

The component provides a consistent centered loading presentation while allowing the message, description, spinner, styling, and standard component properties to be customized.

## Usage

### Basic Usage

```python
import pylage as pl

pl.loading_state()
```

The default state displays the text `Loading...` together with a spinner.

### Custom Text and Description

```python
import pylage as pl

pl.loading_state(
    text="Importing dataset...",
    description="Please wait while your data is parsed and verified.",
)
```

`description` provides secondary context below the primary loading message.

### Reactive Text

```python
import pylage as pl

status = pl.state("Connecting...")
pl.loading_state(text=status)
```

The `text` parameter can receive a reactive `State`, allowing the displayed loading message to participate in the existing PyLage reactive system.

### Spinner Control

```python
import pylage as pl

pl.loading_state(
    text="Synchronizing state",
    spinner=False,
)
```

Set `spinner=False` when the loading presentation should contain text and/or description without the spinner.

### Custom Styling

```python
import pylage as pl

pl.loading_state(
    text="Processing...",
    style=pl.style(
        padding="4rem",
        background_color="#f1f5f9",
    ),
)
```

## API

```python
loading_state(text="Loading...", description=None, spinner=True, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `text` | `Any` | `"Loading..."` | Primary loading message. |
| `description` | `Any` | `None` | Optional secondary loading context. |
| `spinner` | `bool` | `True` | Controls whether the spinner is rendered. |
| `style` | `Style \| None` | `None` | Custom container style merged over the defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the root `Column`. |

## Default Styling

The default container uses a centered vertical layout with:

- `display: flex`
- `flex_direction: column`
- `align_items: center`
- `justify_content: center`
- centered text
- `padding: var(--spacing-2xl)`
- `background_color: var(--color-background)`
- `border_radius: var(--radius-xl)`
- `gap: var(--spacing-sm)`

The primary loading text uses a 1rem font size, medium weight, theme text color, and zero margin.

The optional description uses a smaller muted text style with a maximum width of `24rem`, zero margin, and `1.5` line height.

## Styling Behavior

The optional `style` is merged over the default container style. Supplied values override corresponding defaults while unspecified defaults remain unchanged.

## Composition

The component is composed from existing PyLage engine primitives:

```text
loading_state()
    ↓
Column
    ├── Spinner (optional)
    ├── Text (optional)
    └── Text (optional description)
```

The spinner is added first, followed by the primary text and then the optional description.

## State and Events

`loading_state()` does not define its own event API.

Its `text` and `description` values can participate in the existing PyLage reactive system, including a `State` supplied as the loading text.

## Architecture

`loading_state()` is a UI Kit composition rather than a new rendering primitive.

The implementation creates a `Column`, conditionally adds the existing engine `Spinner`, creates engine `Text` components for the supplied messages, merges the container style, and forwards additional properties to the root `Column`.

## API Boundary

The UI Kit owns the loading-state composition, default presentation, spinner option, text/description handling, and public `loading_state()` entry point.

The underlying engine remains responsible for rendering `Column`, `Spinner`, and `Text`, reactive value handling, styling, and forwarded component properties.

## Verified Working Example

The project demo `demo/demo_loading_state.py` presents three loading-state examples in a responsive grid: dashboard loading with a description, dataset importing with a description, and state synchronization with the spinner enabled.

## Verification

The implementation is covered by `test/components/test_ui_kit_loading_state.py`.

The tests verify:

- the component returns a `Column`
- default container styling
- default loading text and spinner
- custom text and description
- reactive `State` text
- disabling the spinner
- custom style overrides
- forwarding `class_name` and `id` properties

## Verified Sources

- `pylage/UI/components/loading_state.py`
- `demo/demo_loading_state.py`
- `test/components/test_ui_kit_loading_state.py`
- `documents/loading_state.md`

## Status

**Loading State documentation refined and verified.**
