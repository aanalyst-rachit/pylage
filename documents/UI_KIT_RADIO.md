# PyLage UI Kit — Radio

## Overview

`radio_group()` is the public PyLage UI Kit wrapper for the existing PyLage engine `RadioGroup` component.

It provides a Python-first API for grouping native radio inputs without creating a separate renderer, runtime, WebSocket protocol, or reactive engine.

## Import

    import pylage as pl

## Basic Usage

    group = pl.radio_group(
        pl.input(
            input_type="radio",
            name="language",
            value="python",
        ),
        pl.input(
            input_type="radio",
            name="language",
            value="javascript",
        ),
    )

The radio options are existing PyLage input components. The UI Kit reuses the engine RadioGroup implementation.

## State Binding

A reactive `State` can be supplied through `value`.

    selected = pl.State("python")

    group = pl.radio_group(
        pl.input(
            input_type="radio",
            name="language",
            value="python",
        ),
        pl.input(
            input_type="radio",
            name="language",
            value="javascript",
        ),
        value=selected,
    )

The selected radio option follows the current State value.

Changing the State programmatically updates the browser radio selection.

## Change Events

`on_change` uses the existing PyLage event system.

    selected = pl.State("python")

    def handle_change(payload):
        print(payload)

    group = pl.radio_group(
        pl.input(
            input_type="radio",
            name="language",
            value="python",
        ),
        pl.input(
            input_type="radio",
            name="language",
            value="javascript",
        ),
        value=selected,
        on_change=handle_change,
    )

Radio change events provide the existing browser event payload, including the selected value and checked state.

## Native Radio Inputs

Radio options are created with the existing UI Kit input API.

Common properties include:

- `input_type="radio"`
- `name`
- `value`
- `checked`
- `disabled`
- `id`
- native attributes supported by PyLage

## Disabled Options

    pl.radio_group(
        pl.input(
            input_type="radio",
            name="access",
            value="available",
        ),
        pl.input(
            input_type="radio",
            name="access",
            value="locked",
            disabled=True,
        ),
    )

The disabled behavior is handled by the existing native input rendering.

## Architecture

The implementation follows the existing PyLage architecture:

    pylage.UI.components.radio_group
            |
            v
    pylage.ENGINE.RadioGroup
            |
            v
    Existing PyLage renderer
            |
            v
    Existing browser runtime
            |
            v
    Native radio inputs

No separate renderer, reactive engine, WebSocket protocol, or duplicate radio implementation was introduced.

## Verification

Automated RadioGroup verification includes:

- radio option rendering
- option ordering
- group properties
- initial value selection
- State-backed value selection
- change event registration
- reactive registry metadata
- browser interaction
- browser-to-State synchronization
- programmatic State-to-browser synchronization

Manual verification is available in:

    demo/demo_radio.py

Manual coverage includes:

- basic radio groups
- State-bound selection
- change events
- disabled radio options
- native radio attributes

## Status

Complete — Phase 08 Radio

The Radio component has completed implementation, manual verification, automated verification, and documentation.
