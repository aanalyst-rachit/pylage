# PyLage UI Kit — Card

## Definition

`card()` is a semantic UI Kit wrapper around the existing PyLage `Card` primitive. It provides consistent card variants and optional heading, body, and footer convenience arguments while preserving direct composition with existing PyLage components.

## Use

Use `card()` for content containers, information panels, interactive cards, dashboard-style content blocks, and custom composed layouts.

## Usage

### Basic card

Cards can be created directly with existing PyLage components as children:

```python
import pylage as pl

pl.card(
    pl.text("Minimal card", style=pl.style(font_weight="700")),
    pl.text("Simple content container."),
)
```

### Semantic sections

The `heading`, `body`, and `footer` arguments provide convenient semantic content sections. They are optional and can be used independently.

```python
import pylage as pl

pl.card(
    heading="Revenue",
    body="₹42,000",
    footer="Monthly revenue",
)
```

`heading` is converted to a PyLage `Heading`, while `body` and `footer` are converted to PyLage `Text` components.

### Variants

```python
pl.card(heading="Default", variant="default")
pl.card(heading="Elevated", variant="elevated")
pl.card(heading="Outlined", variant="outlined")
pl.card(heading="Interactive", variant="interactive")
```

Supported variants are `default`, `elevated`, `outlined`, and `interactive`.

### Interactive card

Cards can use the existing PyLage event system. An `on_click` callback is forwarded to the underlying card component.

```python
import pylage as pl

count = pl.state(0)

def mark_clicked():
    count.set(count.value + 1)

pl.card(
    heading="Interactive Card",
    body="Click to update the state",
    footer=count,
    variant="interactive",
    on_click=mark_clicked,
)
```

### Advanced composition

Positional children remain fully supported. Existing PyLage components can therefore be composed directly inside the card without introducing separate CardHeader, CardBody, or CardFooter engine components.

```python
import pylage as pl

pl.card(
    pl.column(
        pl.heading("Product Analytics"),
        pl.text("Monthly subscription overview"),
    ),
    pl.column(
        pl.text("Active Users: 1,240"),
        pl.text("Revenue: $4,500"),
    ),
    pl.button("View Full Report"),
    variant="elevated",
)
```

### Custom styling

The `style` argument is merged after the selected variant style, so explicitly supplied style values override matching defaults.

```python
import pylage as pl

pl.card(
    heading="Revenue",
    body="₹42,000",
    style=pl.style(
        background_color="#f8fafc",
        padding="2rem",
    ),
)
```

## API

```python
card(
    *children,
    heading=None,
    body=None,
    footer=None,
    variant="default",
    style=None,
    **props,
)
```

### Parameters

| Parameter | Description |
|---|---|
| `*children` | Existing PyLage child components or other content appended after the optional semantic sections. |
| `heading` | Optional heading content. Non-`None` values are wrapped in the PyLage `Heading` primitive. |
| `body` | Optional body content. Non-`None` values are wrapped in the PyLage `Text` primitive. |
| `footer` | Optional footer content. Non-`None` values are wrapped in the PyLage `Text` primitive. |
| `variant` | Card visual variant. Defaults to `"default"`. |
| `style` | Optional `Style` object merged after the selected variant defaults. |
| `**props` | Additional PyLage engine props and event callbacks forwarded to the underlying `Card`. |

## Validation

`variant` must be one of the supported card variants. An unknown variant raises `ValueError`.

The `variant` argument is consumed by the UI Kit wrapper and is not passed to the underlying engine component as a prop.

## Styling Behavior

Each variant defines its own complete UI Kit baseline:

| Variant | Background | Padding | Radius | Border | Shadow | Cursor |
|---|---|---|---|---|---|---|
| `default` | `var(--color-background)` | `var(--spacing-lg)` | `var(--radius-xl)` | `1px solid var(--color-border)` | none | default |
| `elevated` | `var(--color-background)` | `var(--spacing-lg)` | `var(--radius-xl)` | `1px solid var(--color-border-muted)` | `0 10px 15px -3px rgba(0,0,0,0.1)` | default |
| `outlined` | `var(--color-background)` | `var(--spacing-lg)` | `var(--radius-xl)` | `1px solid var(--color-border-muted)` | none | default |
| `interactive` | `var(--color-background)` | `var(--spacing-lg)` | `var(--radius-xl)` | `1px solid var(--color-border)` | none | `pointer` |

Custom `style` values are merged after the selected variant, giving local styles precedence over variant defaults.

The browser shadow contract verifies that only the `elevated` variant receives a rendered box shadow by default.

## API Boundary

The UI Kit does not introduce a separate Card renderer or section component system. It reuses the existing PyLage `Card`, `Heading`, `Text`, and `Style` primitives and the existing rendering/event infrastructure.

The wrapper is responsible for variant validation, semantic section normalization, variant styling, and custom-style merging.

## Verified Working Examples

The primary Card manual demo covers basic, elevated, interactive, and fully composed cards:

- `demo/demo_card.py`

The semantic API demo specifically exercises `heading`, `body`, `footer`, all four variants, and an interactive state update:

- `demo/demo_card_semantic.py`

`demo/demo_dashboard_card.py` demonstrates the separate `dashboard_card()` component. It is not part of the `card()` API documented here.

## Verification

The implementation is covered by engine, UI Kit, and browser-level tests.

`test/components/test_card.py` verifies the existing Card primitive, children, and forwarded props.

`test/components/test_ui_kit_card.py` verifies:

- existing `Card` component reuse
- default styling
- optional heading, body, and footer sections
- body-only cards
- all four card variants
- custom style precedence
- variant/local style precedence
- forwarded events
- advanced positional children
- prevention of `variant` leakage into engine props
- invalid variant validation

`test/browser/test_card_shadow.py` verifies the rendered browser shadow contract for all four variants.

## Verified Sources

- Component source: `pylage/UI/components/card.py`
- Demo: `demo/demo_card.py`
- Semantic demo: `demo/demo_card_semantic.py`
- Engine test: `test/components/test_card.py`
- UI Kit test: `test/components/test_ui_kit_card.py`
- Browser test: `test/browser/test_card_shadow.py`
- Related component test: `test/components/test_ui_kit_dashboard_card.py`
- Reference documentation: `documents/card.md`

## Status

**Verified and refined.** The documentation reflects the current `card()` implementation, supported variants, semantic arguments, composition model, demos, and test coverage.
