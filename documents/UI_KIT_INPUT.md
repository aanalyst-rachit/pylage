# PyLage UI Kit — Input

## Overview

`pl.input()` provides a Python-first single-line input control for the PyLage UI Kit.

It reuses the existing PyLage engine `Input` component and renderer without introducing a separate rendering or client-side implementation.

## API

    import pylage as ps

    pl.input(
        value="",
        input_type=None,
        style=None,
        **props,
    )

### Parameters

- `value`: Initial input value or a reactive `State`.
- `input_type`: Native HTML input type such as `text`, `email`, `password`, `number`, and others.
- `style`: Standard PyLage `Style` object.
- `**props`: Additional supported PyLage/native input properties and event handlers.

## Basic Usage

    import pylage as ps

    pl.input(
        placeholder="Enter your name...",
    )

## Input Types

The `input_type` argument maps to the existing native HTML input type.

    pl.input(
        input_type="email",
        placeholder="Email address",
    )

    pl.input(
        input_type="password",
        placeholder="Password",
    )

The wrapper passes this through to the existing PyLage engine as `_html_type`.

## State Binding

A `State` can be supplied as the input value.

    import pylage as ps


    name = pl.State("")

    pl.input(
        name,
        placeholder="Your name",
    )

When no explicit `on_input` handler is supplied, the existing PyLage engine automatically updates the supplied `State` from browser input events.

## Event Handling

Input supports the existing PyLage event system.

    def handle_input(payload):
        print(payload)

    pl.input(
        "",
        on_input=handle_input,
    )

Existing event handlers such as `on_change` can also be supplied through normal component properties.

## Common Properties

Input can receive native/common properties through the existing PyLage component API, including:

- `value`
- `placeholder`
- `name`
- `disabled`
- `required`
- `readonly`
- `type`
- `title`
- `minlength`
- `maxlength`

The `input_type` convenience parameter is specifically provided by the UI Kit wrapper for native HTML input types.

## Styling

Input accepts the standard PyLage `Style` object.


    import pylage as ps

    pl.input(
        placeholder="Search...",
        style=pl.style(
            width="100%",
            padding="0.75rem 1rem",
            border="1px solid #cbd5e1",
            border_radius="0.5rem",
            box_sizing="border-box",
        ),
    )

## Disabled State

    pl.input(
        value="This field cannot be edited.",
        disabled=True,
    )

The `disabled` property uses the existing PyLage rendering and native HTML input behavior.

## Architecture

Input follows the existing PyLage architecture:

    PyLage UI Kit
        ↓
    pylage.UI.components.input
        ↓
    Existing PyLage Engine Input
        ↓
    Existing Registry / Renderer
        ↓
    Native <input>

No separate JavaScript renderer, HTML template system, or alternate reactive pipeline is introduced.

## Reuse Decision

Input was classified as **REUSE**.

The existing engine already provides:

- Input component implementation
- Native input rendering
- Input type handling
- State binding
- Browser input/change event handling
- Registry integration
- Client runtime support

The UI Kit layer exposes this existing capability through `pl.input()`.

## Verification

Existing automated Input coverage was executed:

    11 passed

The UI Kit API was also verified directly:

    PASS: UI Kit input imported
    Type: Input

Browser manual verification was performed through the project-wide manual runner:

    pytest -q test/test_all_manuals.py

The UI Kit manual application covers:

- Text input
- Reactive State binding
- Email input
- Password input
- Disabled input
- Required input attribute
- Submit interaction
- PyLage client runtime

Manual application:

    demo/demo_input_features.py

## Status

Input is complete for Phase 08 Forms.

- Reuse audit: Complete
- UI Kit wrapper: Complete
- Automated tests: Complete
- Browser manual verification: Complete
- Documentation: Complete
