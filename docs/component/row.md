# PyLage UI Kit — Row

## Definition

`row()` is the UI Kit layout wrapper for the existing PyLage `Row` component.

The UI Kit does not introduce a separate Row engine, renderer, or reactive system. The underlying Engine `Row` remains the source of truth.

## Use

Use `pl.row()` to arrange child components in a horizontal layout container and control their layout through the existing PyLage style system.

```python
import pylage as pl

content = pl.row(
    pl.text("First"),
    pl.text("Second"),
)
```

## Usage

### Basic row

```python
import pylage as pl

content = pl.row(
    pl.text("First"),
    pl.text("Second"),
    pl.text("Third"),
)
```

Children are passed positionally and preserved in their supplied order.

### Custom styling

```python
import pylage as pl

content = pl.row(
    pl.text("Left"),
    pl.text("Right"),
    style=pl.style(
        gap="1rem",
        justify_content="space-between",
        align_items="center",
    ),
)
```

The style is resolved through the established UI Kit layout styling helpers.

### Responsive styling

`row()` accepts both `Style` and `ResponsiveStyle` values through its `style` parameter. It also accepts the layout wrapper `responsive` input and passes it through the established layout-style builder.

Responsive behavior therefore remains part of the existing style infrastructure rather than introducing Row-specific responsive logic.

### Filtering `None` children

`None` children are removed before the underlying Engine `Row` is constructed.

```python
import pylage as pl

content = pl.row(
    pl.text("A"),
    None,
    pl.text("B"),
)
```

Only the actual component children are passed to the Engine Row.

## API

```python
row(*children: Any, style: Style | ResponsiveStyle | None = None, **props: Any) -> Component
```

### Parameters

- `*children` — positional child components. `None` values are filtered out.
- `style` — optional `Style` or `ResponsiveStyle` used by the established UI Kit layout-style builder.
- `**props` — additional component properties forwarded to the underlying Engine Row.
- `responsive` — consumed by the UI Kit wrapper and incorporated into the resolved layout style.

## Behavior

The implementation performs three layout-wrapper responsibilities:

1. It removes `None` values from the supplied children.
2. It extracts the wrapper-level `responsive` input.
3. It builds the final layout style and delegates to the existing Engine `Row`.

The Engine implementation is simply:

```python
def Row(*children, **props: Any) -> Component:
    return component("Row", *children, **props)
```

## Styling

Row uses the existing UI Kit layout-style infrastructure. Custom layout properties such as `gap`, `justify_content`, `align_items`, `flex_wrap`, `width`, and padding can be supplied through `pl.style(...)`.

The manual Row demo verifies common horizontal layout use cases including gap, justification, alignment, flex wrapping, and an interactive navigation row.

## API Boundary

`pl.row()` is a UI Kit wrapper; it does not replace or modify the Engine `Row` implementation.

The same Engine Row is also used internally by higher-level layout patterns such as Split, TwoColumn, and ThreeColumn. Their individual contracts remain separate from this document.

## Verified Working Examples

The primary manual example is `demo/demo_row.py`.

It covers:

- basic horizontal child layout
- gap styling
- `justify_content` and `align_items`
- flex wrapping
- interactive children using `pl.state` callbacks

## Verification

Row-specific UI Kit coverage is provided by `test/components/test_ui_kit_row.py`, with additional layout API and regression coverage in the test suite.

The canonical Row documentation is considered valid only after the focused Row tests and documentation checks pass.

## Verified Sources

- `pylage/UI/layout/row.py`
- `pylage/ENGINE/components/basic.py`
- `test/components/test_ui_kit_row.py`
- `test/components/test_ui_kit_layout_api.py`
- `demo/demo_row.py`

## Status

Canonical Row documentation refined from the helper documentation and verified against the current implementation and test/demo sources.
