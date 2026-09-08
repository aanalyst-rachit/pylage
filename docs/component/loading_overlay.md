# PyLage UI Kit — Loading Overlay

## Definition

`loading_overlay` is a reusable PyLage UI Kit recipe for displaying a blocking, full-viewport loading state.

It reuses the existing `Dialog`, `Column`, `Spinner`, and `Text` components instead of introducing a separate rendering primitive.

## Use

Use `loading_overlay()` when an application needs to indicate that an operation is in progress while presenting a blocking loading state over the current page.

The overlay supports boolean or reactive visibility, optional loading text, optional spinner rendering, custom styling, and properties forwarded to the underlying `Dialog`.

## Usage

### Basic Usage

```python
import pylage as pl

pl.loading_overlay(open=True)
```

By default, the overlay displays a spinner and the text `Loading...`.

### Custom Text

```python
pl.loading_overlay(
    "Saving changes...",
    open=True,
)
```

Pass `text=None` to omit the loading message.

### Spinner Control

```python
pl.loading_overlay(
    "Loading data...",
    open=True,
    spinner=False,
)
```

The spinner is enabled by default. Set `spinner=False` to omit it.

### Reactive Visibility

```python
loading = pl.state(False)

pl.loading_overlay(
    "Please wait...",
    open=loading,
)
```

The existing PyLage reactive runtime reflects changes to the supplied state in the rendered Dialog.

### Forwarded Dialog Properties

Additional properties are forwarded through `**props` to the underlying `Dialog`.

```python
pl.loading_overlay(
    "Please wait...",
    open=True,
    title="Loading overlay",
    class_name="custom-loading-overlay",
)
```

## API

```python
loading_overlay(text="Loading...", open=False, spinner=True, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `text` | `Any` | `"Loading..."` | Loading message. Pass `None` to omit it. |
| `open` | `Any` | `False` | Controls Dialog visibility and may receive a reactive state. |
| `spinner` | `bool` | `True` | Controls whether the spinner is rendered. |
| `style` | `Style \| None` | `None` | Custom overlay style merged over the default style. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Dialog`. |

## Default Styling

The overlay uses a full-viewport style with fixed positioning, zero offsets, `100vw` width, and `100vh` height.

Default overlay properties include:

- `max_width: none` and `max_height: none`
- zero margin and padding
- `box_sizing: border-box`
- semi-transparent black background
- no border and zero border radius
- `z_index: 1100`
- text color from `var(--color-text)`

The content column also occupies the viewport and centers its children horizontally and vertically. It uses column layout, spacing, padding, and centered text.

## Styling Behavior

The optional `style` is merged with the default overlay style. Supplied values override corresponding defaults while unspecified defaults remain in place.

```python
pl.loading_overlay(
    "Working...",
    open=True,
    style=pl.style(
        z_index=2000,
        background_color="rgba(0, 0, 0, 0.7)",
    ),
)
```

## Composition

The recipe is composed from existing PyLage primitives:

```text
loading_overlay()
    ↓
Dialog
    ↓
Column
    ├── Spinner (optional)
    └── Text (optional)
```

When `spinner=False`, the spinner is omitted. When `text=None`, the text component is omitted.

## State and Events

The `open` parameter accepts a boolean or reactive `State`. State changes are reflected through the existing Dialog rendering behavior.

The loading overlay does not define a separate event API. Dialog properties and supported behavior can be supplied through `**props`.

## Architecture

`loading_overlay()` is a reusable UI Kit recipe rather than a new rendering primitive.

The implementation creates a `Column` containing the optional spinner and text, then passes that content to the existing `dialog()` component with the overlay style.

## API Boundary

The UI Kit owns the loading-overlay composition, default viewport styling, spinner/text options, and public `loading_overlay()` entry point.

The underlying engine remains responsible for Dialog rendering, native output, reactive state handling, and forwarded properties.

## Verified Working Example

The project demo `demo/demo_loading_overlay.py` provides a manual test page with a reactive loading state and a Start / Stop Loading button. It uses the message `"Please wait..."`, keeps the spinner enabled, and forwards a Dialog title.

The demo also keeps the underlying page content mounted while the overlay is toggled.

## Verification

The implementation is covered by `test/components/test_ui_kit_loading_overlay.py`.

The tests verify:

- Dialog-based component construction
- closed-by-default behavior
- boolean `open` control
- reactive `State` visibility
- spinner and text rendering
- disabling the spinner
- full-viewport positioning and content alignment
- custom style overrides
- forwarded Dialog properties
- Column content preservation
- rendered Dialog content and viewport styles
- public UI Kit export

## Verified Sources

- `pylage/UI/components/loading_overlay.py`
- `demo/demo_loading_overlay.py`
- `test/components/test_ui_kit_loading_overlay.py`
- `documents/loading_overlay.md`

## Status

**Loading Overlay documentation refined and verified.**
