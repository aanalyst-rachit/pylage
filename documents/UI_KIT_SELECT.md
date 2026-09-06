# UI Kit Select

## Overview

`pylage.UI.select` is the public PyLage UI Kit wrapper for the existing engine `Select` component.

It provides a Python-first dropdown/select control without introducing a separate renderer or runtime implementation.

## API

    import pylage as pl
    import pylage as pl

    pl.select(
        pl.Option("India", value="india"),
        pl.Option("Japan", value="japan"),
        value="india",
    )

## Parameters

The UI Kit wrapper accepts:

- `*children` — `Option` components or other supported children.
- `style` — optional PyLage `Style`.
- `**props` — existing engine Select properties and event handlers.

Common properties include:

- `value`
- `multiple`
- `size`
- `name`
- `disabled`
- `required`
- `title`
- `on_change`

## Options

Use the existing engine `Option` component:

    import pylage as pl

    pl.select(
        pl.Option("India", value="india"),
        pl.Option("Japan", value="japan"),
    )

Option labels and values are rendered through the existing Select renderer.

## State Binding

The existing engine Select accepts PyLage `State` values:

    import pylage as pl
    import pylage as pl

    country = pl.State("india")

    country_select = pl.select(
        pl.Option("India", value="india"),
        pl.Option("Japan", value="japan"),
        value=country,
    )

State and browser event handling remain owned by the existing PyLage engine.

## Change Events

Custom change handlers can be supplied through `on_change`:

    def handle_change(payload):
        print(payload)

    pl.select(
        pl.Option("India", value="india"),
        pl.Option("Japan", value="japan"),
        on_change=handle_change,
    )

The existing browser runtime provides the Select event payload.

## Multiple Selection

Native multiple selection is supported:

    pl.select(
        pl.Option("Python", value="python"),
        pl.Option("JavaScript", value="javascript"),
        pl.Option("Rust", value="rust"),
        multiple=True,
        size=3,
    )

## Disabled State

The existing engine supports native disabled behavior:

    pl.select(
        pl.Option("Unavailable", value="unavailable"),
        value="unavailable",
        disabled=True,
    )

## Styling

The wrapper accepts the existing PyLage `Style` object:

    import pylage as pl

    pl.select(
        pl.Option("India", value="india"),
        pl.Option("Japan", value="japan"),
        style=pl.style(
            width="100%",
            padding="0.75rem",
        ),
    )

No separate Select styling system was introduced.

## Architecture

    User Application
          ↓
    pylage-ui-kit
          ↓
    pylage.UI.select
          ↓
    pylage.ENGINE.Select
          ↓
    existing renderer/runtime
          ↓
    browser <select>

## Reuse Decision

**Decision: REUSE**

The Select capability already existed in the PyLage engine and already provided:

- Select rendering
- Option rendering
- value support
- multiple selection
- additional native properties
- State-compatible usage
- browser change events
- existing renderer/runtime integration

Therefore no new renderer, runtime, reactive engine, or duplicate Select implementation was required.

The UI Kit layer exposes the existing capability through the public `pl.select()` wrapper.

## Manual Application

Dedicated manual application:

    demo/demo_select_features.py

The manual application covers:

- Basic Select
- State-bound Select
- Custom `on_change` handler
- Disabled Select
- Multiple Select
- Native Select properties

## Verification

Automated Select-related verification:

    18 passed in 0.63s

Project-wide browser/manual verification:

    pytest -q test/test_all_manuals.py
    1 passed in 65.61s

The project-wide manual runner completed successfully and the Select manual behavior was verified.

## Status

**Complete — Phase 08 Select**
