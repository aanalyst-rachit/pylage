# First App

## Definition

The `playground/` directory contains the canonical public showcase application for the current PyLage release.

The playground demonstrates a complete PyLage application built with the public `pylage` API, including reactive state, navigation, components, layouts, overlays, tables, forms, themes, and server-driven updates.

## Requirements

- Use the project virtual environment.
- Run commands from the repository root.
- The current repository package is imported as `pylage`.

## Application Structure

```text
playground/
├── __init__.py
├── app.py
├── runtime.py
└── server.py
```

The application factory is defined in `playground/app.py`.

The local playground server is defined in `playground/server.py`.

## Application Factory

The playground exposes `get_app()`, which creates the complete showcase application.

The factory builds the application UI with the public:

```python
import pylage as pl
```

API boundary.

The application demonstrates reactive state, navigation, page content, components, layouts, overlays, tables, forms, and theme capabilities.

## Launching the Playground

From the repository root:

```bash
.venv/bin/python -m playground.server
```

The development playground server starts on:

```text
http://127.0.0.1:8000
```

The server opens the playground in the default browser and can be stopped with `Ctrl+C`.

## Public API Boundary

Application code imports the public package namespace:

```python
import pylage as pl
```

The playground uses public APIs such as:

```python
pl.dashboard(...)
pl.navigation(...)
pl.navigation_item(...)
pl.state(...)
pl.derived(...)
pl.column(...)
pl.row(...)
pl.form(...)
pl.table(...)
pl.drawer(...)
pl.modal(...)
pl.toast(...)
pl.set_theme(...)
```

Internal `pylage.ENGINE` APIs are implementation details and are not required for normal application development.

## Repository Verification

From the repository root:

```bash
.venv/bin/python -c "import pylage; print('PYLAGE IMPORT: PASS'); print(pylage.__file__)"
.venv/bin/python -c "import playground.app as app; print('PLAYGROUND IMPORT: PASS'); print('APP FACTORY:', callable(app.get_app))"
```

Both imports should resolve against the current repository checkout.

## Verification

The first-app documentation is based on the current `playground/` application and its server entry point.

For the interactive showcase, use:

```bash
.venv/bin/python -m playground.server
```

For application-level API verification, import `playground.app` and call `get_app()` through the project virtual environment.

## Verified Sources

- `playground/app.py` — canonical showcase application and application factory.
- `playground/server.py` — local playground server and launch configuration.
- `playground/runtime.py` — playground-specific runtime integration.
- `playground/__init__.py` — public playground package entry point.

## Status

This guide reflects the current PyLage V2 public-release playground and public `pylage` API.
