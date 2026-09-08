# PyLage UI Kit — Badge

## Definition

`badge()` is a semantic UI Kit wrapper around the existing PyLage `Badge` primitive. It provides compact status/category styling while preserving the existing PyLage rendering, component composition, state, props, and event systems.

## Use

Use `badge()` for short status labels, categories, states, counters, or other compact pieces of contextual information.

## Usage

### Basic badge

```python
import pylage as pl

pl.badge("Active")
```

### Variants

```python
pl.badge("Default")
pl.badge("Primary", variant="primary")
pl.badge("Secondary", variant="secondary")
pl.badge("Success", variant="success")
pl.badge("Warning", variant="warning")
pl.badge("Danger", variant="danger")
pl.badge("Info", variant="info")
```

Supported variants are `default`, `primary`, `secondary`, `success`, `warning`, `danger`, and `info`.

### Component content

Existing PyLage components can be passed as children. Primitive values are normalized through the existing `Text` primitive.

```python
import pylage as pl

pl.badge(pl.text("Active"))
```

### Reactive content

Badges can display existing PyLage state values. The UI Kit preserves the generated child component so the existing state/rendering system can update the displayed value.

```python
import pylage as pl

count = pl.state(3)
pl.badge(count, variant="secondary")
```

### Custom styling

The `style` argument is merged after the UI Kit defaults, so explicitly supplied style values override matching defaults.

```python
import pylage as pl

pl.badge(
    "Custom",
    style=pl.style(
        font_size="0.875rem",
        padding="0.5rem 0.75rem",
    ),
)
```

### Props and events

Additional PyLage engine props and event callbacks are forwarded to the underlying `Badge` component.

```python
pl.badge(
    "Active",
    class_name="status-badge",
    title="Current status",
)
```

Event callbacks such as `on_click` are also forwarded through the existing PyLage event system.

## API

```python
badge(*children, variant="default", style=None, **props)
```

### Parameters

| Parameter | Description |
|---|---|
| `*children` | Badge content. Existing `Component` instances are preserved; other non-`None` values are wrapped with the existing `Text` primitive. |
| `variant` | Semantic visual variant. Defaults to `"default"`. |
| `style` | Optional `Style` object merged after the UI Kit defaults. |
| `**props` | Additional PyLage engine props and event callbacks forwarded to the underlying `Badge`. |

## Validation

`variant` must be one of the supported variants. An unknown variant raises `ValueError`.

The `variant` argument is consumed by the UI Kit wrapper and is not passed through as an engine prop.

## Styling Behavior

The badge starts with these common UI Kit defaults:

- `padding`: `0.25rem 0.625rem`
- `border_radius`: `var(--radius-full)`
- `font_size`: `0.75rem`
- `font_weight`: `600`

Each variant then supplies its semantic background, foreground, and border styling:

| Variant | Background | Text | Border |
|---|---|---|---|
| `default` | `var(--color-surface-variant)` | `var(--color-text)` | `var(--color-border)` |
| `primary` | `var(--color-primary)` | `var(--color-primary-contrast)` | `var(--color-primary)` |
| `secondary` | `var(--color-secondary)` | `var(--color-secondary-contrast)` | `var(--color-secondary)` |
| `success` | `var(--color-success)` | `var(--color-primary-contrast)` | `var(--color-success)` |
| `warning` | `var(--color-warning)` | `var(--color-text)` | `var(--color-warning)` |
| `danger` | `var(--color-danger)` | `var(--color-primary-contrast)` | `var(--color-danger)` |
| `info` | `var(--color-info)` | `var(--color-primary-contrast)` | `var(--color-info)` |

The merge order is base style → variant style → custom `style`. Therefore custom styling has final precedence for overlapping properties.

## API Boundary

The UI Kit does not introduce a separate Badge renderer, styling engine, or state system. It reuses the existing PyLage `Badge`, `Text`, `Component`, `Style`, and rendering infrastructure.

The wrapper is responsible for semantic defaults, variant validation, child normalization, and style merging.

## Verified Working Examples

The primary Badge demo covers all supported variants:

- `demo/demo_badge.py`

A broader manual integration demo verifies badges with reactive `State` values alongside other UI components:

- `demo/demo_avatar_badge_divider.py`

## Verification

The implementation is covered by both engine-level and UI Kit tests.

`test/components/test_badge.py` verifies the existing Badge primitive, children, and forwarded props.

`test/components/test_ui_kit_badge.py` verifies the UI Kit contract, including:

- existing `Badge` component reuse
- default styling
- rendered text content
- reactive state content
- text-child normalization
- reactive child identity preservation
- all supported variants
- custom style precedence
- prevention of `variant` leakage into engine props
- forwarded engine props
- forwarded events
- invalid variant validation

## Verified Sources

- Component source: `pylage/UI/components/badge.py`
- Demo: `demo/demo_badge.py`
- Integration demo: `demo/demo_avatar_badge_divider.py`
- Engine test: `test/components/test_badge.py`
- UI Kit test: `test/components/test_ui_kit_badge.py`
- Reference documentation: `documents/badge.md`

## Status

**Verified and refined.** The documentation reflects the current Badge implementation, supported API, demos, and test coverage.
