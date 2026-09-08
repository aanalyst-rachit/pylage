# PyLage UI Kit — Column

## Definition

`column()` is the public PyLage UI Kit layout wrapper for the existing Engine `Column` component.
It provides vertical child composition while reusing PyLage's existing rendering, responsive styling, and reactive State infrastructure.

## Use

Use `column()` when child components should be arranged as a vertical layout container.

- Stack multiple components vertically
- Control spacing with `gap`
- Align children horizontally with `align_items`
- Distribute children vertically with `justify_content`
- Create fixed-height or scrollable content areas
- Apply normal or responsive styles
- Use reactive `State` values inside styles
- Forward standard component properties such as `class_name` and `title`

## Usage

### Basic column

```python
import pylage as pl

content = pl.column(
    pl.text("First item"),
    pl.text("Second item"),
    pl.text("Third item"),
)
```

Children are rendered in vertical order.

### Spacing with `gap`

The wrapper provides a default `gap` through the UI Kit layout style system. A local `Style` can override it.

```python
import pylage as pl

content = pl.column(
    pl.text("Item 1"),
    pl.text("Item 2"),
    pl.text("Item 3"),
    style=pl.style(gap="0.75rem"),
)
```

### Child alignment

Use `align_items` to control the horizontal alignment of children in the vertical column.

```python
import pylage as pl

content = pl.column(
    pl.text("Centered item"),
    pl.text("Another item"),
    style=pl.style(
        align_items="center",
        gap="0.75rem",
    ),
)
```

### Vertical distribution

Use `justify_content` when the column has available vertical space to distribute.

```python
import pylage as pl

content = pl.column(
    pl.text("Top"),
    pl.text("Bottom"),
    style=pl.style(
        height="180px",
        justify_content="space-between",
    ),
)
```

### Scrollable column

A fixed-height column can be made scrollable through normal style properties.

```python
import pylage as pl

content = pl.column(
    pl.text("Item 1"),
    pl.text("Item 2"),
    pl.text("Item 3"),
    pl.text("Item 4"),
    style=pl.style(
        height="140px",
        overflow="auto",
        gap="0.5rem",
    ),
)
```

### Reactive style

`State` values can be placed inside a `Style` and resolved reactively.

```python
import pylage as pl

gap = pl.state("1rem")

content = pl.column(
    pl.text("Reactive content"),
    style=pl.style(gap=gap),
)
```

The repository's reactive demo changes the column gap between `1rem` and `2rem` and also updates the column background color through State-backed style values.

### Responsive styling

`column()` accepts `ResponsiveStyle` through the `style` parameter and also supports the UI Kit's `responsive` style input.

The responsive value is passed through the existing UI Kit layout-style resolution system rather than introducing a separate responsive implementation.

## API

```python
column(*children, style=None, **props)
```

### Parameters

| Parameter | Description |
|---|---|
| `*children` | Child components or values passed to the underlying Engine `Column`. `None` children are filtered out. |
| `style` | Optional `Style` or `ResponsiveStyle` used to customize the column layout. |
| `**props` | Additional properties forwarded to the underlying Engine `Column`. The special `responsive` property is consumed by the UI Kit responsive style pipeline. |

## Default Styling

The wrapper builds its layout style through the existing UI Kit responsive-style system.

The verified default layout includes:

| Property | Default |
|---|---|
| `gap` | `var(--spacing-md)` |

A locally supplied `style` value overrides the corresponding default. For example, `Style(gap="12px")` replaces the default `var(--spacing-md)` gap.

## Behavior

- Existing `Component` children are preserved.
- `None` children are removed before creating the Engine `Column`.
- Additional props such as `class_name` and `title` are forwarded.
- The wrapper returns an existing Engine `Column` represented as a PyLage `Component`.
- The resulting Engine component renders as a `<div>` container.
- Reactive `State` values nested inside styles are resolved by the existing PyLage styling/reactivity system.

## API Boundary

The UI Kit wrapper delegates layout rendering to the existing Engine:

```text
pylage.UI.layout.column
        ↓
pylage.ENGINE.components.basic.Column
        ↓
PyLage renderer / responsive style system / runtime
        ↓
Browser DOM
```

No duplicate column renderer or separate layout engine is introduced by the wrapper.

## Verified Working Examples

- `demo/demo_column.py` — vertical stacking, gap, child alignment, `justify_content`, fixed-height scrolling, and interactive State content.
- `demo/demo_column_reactive.py` — wrapper reuse, child composition, forwarded props, and reactive gap/background style updates.

## Verification

### Automated tests

Verified coverage includes:

- `test/components/test_column.py` — Engine Column rendering and forwarded properties.
- `test/components/test_ui_kit_column.py` — UI Kit wrapping, rendering, props, styles, default gap, style override, reactive style values, child preservation, `None` filtering, and public export.

### Manual verification

The repository reference records manual verification of reactive `gap` changes from `1rem` to `2rem` and reactive background-color changes. State-backed values nested inside `Style` also have regression coverage.

## Verified Sources

- Component: `pylage/UI/layout/column.py`
- Demo: `demo/demo_column.py`
- Reactive demo: `demo/demo_column_reactive.py`
- Engine tests: `test/components/test_column.py`
- UI Kit tests: `test/components/test_ui_kit_column.py`
- Reference: `docs/helper/column.md`

## Status

**FINAL / VERIFIED** — documentation reflects the current `column()` implementation, verified demos, and available automated tests.
