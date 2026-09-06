# UI Kit Loading State

`pylage.loading_state()` provides a semantic, high-level loader and spinner feedback card for data fetching and async operations.

## Basic Usage

```python
import pylage as pl

pl.loading_state()
```

## Custom Text and Description

```python
import pylage as pl

pl.loading_state(
    text="Importing dataset...",
    description="Please wait while your data is parsed and verified.",
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `text` | `Any` | `"Loading..."` | Primary loading indicator label |
| `description` | `Any` | `None` | Optional subtitle or secondary context message |
| `spinner` | `bool` | `True` | Whether to display the animated spinner component |
| `style` | `Style` | `None` | Style overrides merged with default container style |
| `**props` | `Any` | — | Forwarded to root component |

## Reactive Binding

```python
import pylage as pl

status = pl.State("Connecting...")
pl.loading_state(text=status)
```

## Loading Overlay

`pylage.UI.loading_overlay()` provides a blocking, full-viewport loading overlay for operations that temporarily prevent interaction with the underlying page.

### Basic Usage

```python
import pylage as pl

overlay = pl.loading_overlay(
    text="Please wait...",
    open=True,
    spinner=True,
)
```

### Reactive Visibility

```python
import pylage as pl

loading = pl.State(False)
overlay = pl.loading_overlay(
    text="Please wait...",
    open=loading,
    spinner=True,
)
```

The `open` property can be bound to `State`, allowing the overlay to reactively appear and disappear.

### Behavior

- Covers the full viewport while open.
- Blocks interaction with the underlying page while open.
- Displays the animated PyLage Spinner by default.
- Displays optional loading text below the spinner.
- Uses the existing Dialog component as its root.
- Supports `spinner=False` when only loading text is required.
- Accepts `style` overrides and forwarded component properties.

The overlay is intentionally blocking while open; underlying controls are expected to become interactive again after the loading state is set to `False`.
