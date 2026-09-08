# PyLage UI Kit — Migration from Low-Level PyLage API

## Purpose

PyLage UI Kit provides the high-level Python-first application API over the existing PyLage runtime, components, styling, themes, layouts, patterns, and templates.

Applications should prefer the canonical `pylage as pl` public surface instead of importing internal engine or implementation modules directly.

## Canonical Public API

Use lowercase public APIs from `pylage`:

- `pl.button()`
- `pl.card()`
- `pl.text()`
- `pl.heading()`
- `pl.input()`
- `pl.select()`
- `pl.form()`
- `pl.form_field()`
- `pl.checkbox()`
- `pl.badge()`
- `pl.alert()`
- `pl.dialog()`
- `pl.drawer()`
- `pl.tabs()`
- `pl.table()`
- `pl.row()`
- `pl.column()`
- `pl.state()`
- `pl.image()`
- `pl.option()`

## Migration Rules

### Prefer the public `pl.*` surface

Application code should use the documented lowercase `pl.*` APIs.

### Low-level PyLage components

Existing low-level PyLage component APIs remain supported for compatibility. When an equivalent UI Kit API exists, new application code should prefer the UI Kit wrapper or composition API.

### Internal Engine APIs

Do not build application code around `pylage.ENGINE.*` implementation modules. These are internal implementation details rather than the recommended UI Kit application surface.

### Legacy UI aliases and examples

| Legacy form | Canonical form |
| --- | --- |
| `ui.button(...)` | `pl.button(...)` |
| `ui.data_list(...)` | `pl.data_list(...)` |
| `ui.metric(...)` | `pl.metric(...)` |
| `ps.metric()` | `pl.metric()` |
| `ps.alert()` | `pl.alert()` |
| `ps.dialog()` | `pl.dialog()` |
| `ps.tabs()` | `pl.tabs()` |
| `ps.table()` | `pl.table()` |

## State Migration

Use the lowercase public state API:

```python
import pylage as pl

count = pl.state(0)
```

The existing PyLage State implementation remains the source of truth. The lowercase API is the public compatibility surface.

## Image and Option Migration

Use the lowercase public helpers:

```python
import pylage as pl

image = pl.image(src="/static/example.png")
item = pl.option("Example", value="example")
```

## Styling and Theme Migration

Continue using the existing Style, Theme, token, and ResponsiveStyle systems. Migration does not introduce a second styling or theme engine.

## Compatibility

Migration is additive. Existing low-level PyLage APIs continue to work where supported. The purpose of this migration is to provide a stable, documented, high-level application surface rather than remove the underlying PyLage APIs.

## Migration Checklist

- [ ] Replace legacy `ui.*` application examples with `pl.*`.
- [ ] Replace stale `ps.*` application examples with `pl.*`.
- [ ] Prefer lowercase public APIs.
- [ ] Use `pl.state()` for public state access.
- [ ] Use `pl.image()` for the public image helper.
- [ ] Use `pl.option()` for the public option helper.
- [ ] Keep internal `pylage.ENGINE.*` references only when documenting implementation/source architecture.
- [ ] Keep low-level `pylage.components.*` references only when documenting compatibility or implementation architecture.

## Verification

Migration documentation is verified against the current public API exports and the UI Kit API conventions.
