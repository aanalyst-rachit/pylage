# PyLage UI Kit — Tooltip

## Definition

`tooltip()` is the UI Kit recipe wrapper for the existing PyLage `Tooltip` component.

The UI Kit does not introduce a separate tooltip renderer, interaction engine, or client-side tooltip implementation. The existing Engine Tooltip remains the source of truth.

## Use

Use `pl.tooltip()` when an existing component should expose tooltip information through the existing PyLage Tooltip behavior.

```python
import pylage as pl

content = pl.tooltip(
    pl.text("Info"),
    title="Helpful information",
)
```

The supplied child remains the tooltip target, while the supplied properties are forwarded to the existing Tooltip component.

## Usage

### Tooltip on a button

```python
import pylage as pl

content = pl.tooltip(
    pl.button("Hover target"),
    title="Helpful information",
)
```

### Tooltip on text

```python
import pylage as pl

content = pl.tooltip(
    pl.text("Hover over this information target"),
    title="Additional information",
)
```

### Multiple children and properties

```python
import pylage as pl

content = pl.tooltip(
    pl.text("Info"),
    pl.button("Action"),
    class_name="tooltip",
    title="Quick help",
)
```

Existing child and component properties are preserved through the wrapper.

## API

```python
tooltip(*children: Any, **props: Any) -> Component
```

- `*children` — child components passed to the underlying Engine Tooltip.
- `**props` — properties forwarded unchanged to the underlying Engine Tooltip.

Commonly verified properties include `title` and `class_name`.

## Behavior

The UI Kit implementation delegates directly to the Engine Tooltip:

```python
def tooltip(*children: Any, **props: Any) -> Component:
    return _Tooltip(*children, **props)
```

The underlying Engine implementation delegates to the standard component factory:

```python
def Tooltip(*children, **props: Any) -> Component:
    return component("Tooltip", *children, **props)
```

Therefore tooltip rendering and property handling remain part of the existing PyLage component and renderer infrastructure.

## Rendering Contract

Current UI Kit tests verify that Tooltip renders with the supplied child content and forwards `title` and `class_name` properties.

The verified rendered representation uses the existing Tooltip component rather than introducing tooltip-specific markup in the UI Kit recipe.

## API Boundary

`pl.tooltip()` is a recipe-level wrapper only.

It does not:

- implement a second Tooltip component
- add a separate renderer
- add client-side tooltip JavaScript
- introduce a tooltip-specific reactive system

Existing PyLage Tooltip behavior remains the implementation boundary.

## Verified Working Examples

The primary manual example is `demo/demo_tooltip.py`.

It demonstrates Tooltip usage with:

- a Button target
- a Text target
- `title` tooltip content
- `class_name` forwarding

## Verification

Tooltip-specific UI Kit coverage is provided by `test/components/test_ui_kit_tooltip.py`.

The canonical documentation is considered valid only after the focused Tooltip tests and repository documentation checks pass.

## Verified Sources

- `pylage/UI/recipes/tooltip.py`
- `pylage/ENGINE/components/basic.py`
- `test/components/test_ui_kit_tooltip.py`
- `demo/demo_tooltip.py`

## Status

Canonical Tooltip documentation refined from the helper documentation and verified against the current implementation and test/demo sources.
