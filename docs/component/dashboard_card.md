# PyLage UI Kit — Dashboard Card

## Definition

`dashboard_card()` is a high-level PyLage UI Kit card wrapper designed for dashboard widgets.
It provides structured title, action, body, content, and footer areas while reusing the existing `card()` component for the final card surface.

## Use

Use `dashboard_card()` for dashboard-oriented information panels where common widget structure is useful.

- Display a dashboard widget title
- Add a contextual action or status badge
- Display descriptive body text
- Embed existing components such as metrics or other widgets
- Display footer metadata or status information
- Reuse the existing card variants and styling system
- Customize the resulting card through `style` and standard component properties

## Usage

### Basic dashboard card

```python
import pylage as pl

card = pl.dashboard_card(
    title="Real-time Traffic",
    body="14,200 sessions actively streaming.",
    footer="Refreshed 10s ago",
)
```

### Card with an action

The `action` value is placed alongside the title in a horizontal header row.

```python
import pylage as pl

card = pl.dashboard_card(
    title="Active Users",
    body="3,420 active right now.",
    action=pl.badge("Live", variant="success"),
    footer="Refreshed every 30s",
)
```

### Embedded components

Positional children are added after the optional body and before the optional footer. This allows components such as metrics to be embedded directly inside the card.

```python
import pylage as pl

card = pl.dashboard_card(
    pl.metric(label="Active Containers", value="94/100", delta="+6"),
    title="Fleet Capacity",
    action=pl.badge("Healthy", variant="success"),
    footer="Cluster: us-west-prod",
)
```

### Component content

`title`, `body`, and `footer` can receive existing components instead of plain strings.

- Component titles are preserved directly.
- Non-string body values are preserved directly.
- Non-string footer values are preserved directly.
- String body values are converted to `Text`.
- String footer values are converted to muted, small `Text`.

### Custom styling

The `style` parameter is passed to the underlying `card()` wrapper, allowing the card surface to be customized.

```python
import pylage as pl

card = pl.dashboard_card(
    title="Custom Card",
    body="Dashboard content",
    style=pl.style(
        background_color="#f8fafc",
        padding="2rem",
    ),
)
```

## API

```python
dashboard_card(
    *children,
    title=None,
    body=None,
    footer=None,
    action=None,
    variant="elevated",
    style=None,
    **props,
)
```

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `*children` | — | Positional child components added after the body and before the footer. |
| `title` | `None` | Title text or component. String-like truthy values are wrapped in an Engine level-3 `Heading`; component values are preserved. |
| `body` | `None` | Primary body content. Strings are converted to `Text`; other values are preserved. |
| `footer` | `None` | Footer content. Strings are converted to small muted `Text`; other values are preserved. |
| `action` | `None` | Optional action or status component placed beside the title. |
| `variant` | `"elevated"` | Card surface variant passed to the underlying `card()` component. |
| `style` | `None` | Optional `Style` passed to the underlying `card()` component. |
| `**props` | — | Additional properties forwarded to the underlying `card()` component. |

## Composition Behavior

The internal content order is:

```text
title / action header
        ↓
body
        ↓
positional children
        ↓
footer
```

When either `title` or `action` is supplied, a header area is created.
If only a title is present, the title can be inserted directly. When both title and action are present, they are placed in a horizontal Engine `Row` with space-between alignment.

The title header uses a level-3 Engine `Heading` with the internal title style when a title value is converted from plain content.

Footer strings use a small muted text style.

## Variant and Styling Behavior

`dashboard_card()` does not implement a separate card-surface styling system. Its `variant`, `style`, and additional properties are delegated to the existing `card()` wrapper.

This keeps dashboard cards consistent with the standard PyLage card behavior and styling contract.

## API Boundary

`dashboard_card()` is a composition wrapper rather than a separate rendering engine.

```text
pylage.UI.components.dashboard_card.dashboard_card
        ↓
pylage.UI.components.card.card
        ↓
PyLage Engine Card
        ↓
PyLage renderer / runtime
        ↓
Browser DOM
```

## Verified Working Examples

- `demo/demo_dashboard_card.py` — dashboard cards with titles, body content, contextual badges, action buttons, footers, and dashboard-grid composition.

## Verification

### Automated tests

`test/components/test_ui_kit_dashboard_card.py` verifies:

- The wrapper returns an Engine `Card`.
- Title, body, and footer content render correctly.
- Action components render correctly.
- Custom styles reach the resulting card style.

## Verified Sources

- Component: `pylage/UI/components/dashboard_card.py`
- Demo: `demo/demo_dashboard_card.py`
- Test: `test/components/test_ui_kit_dashboard_card.py`
- Reference: `documents/dashboard_card.md`

## Status

**FINAL / VERIFIED** — documentation reflects the current `dashboard_card()` implementation, verified demo usage, and available automated coverage.
