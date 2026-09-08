# First App

## Definition

The `working_demo/` directory is the repository's actual working application and serves as the canonical first-app example for the PyLage UI Kit.

The application demonstrates a complete PyLage UI Kit application built with the public `pylage` API.

## Requirements

- Use the project virtual environment.
- Run commands from the repository root.
- The current repository package is imported as `pylage`.

## Application Structure

The working application is organized as a Python package:

```text
working_demo/
├── __init__.py
└── app.py
```

The application implementation is in `working_demo/app.py`.

## Application Factory

The application exposes `get_app()`, which creates the complete dashboard application.

The factory creates reactive navigation state, page content, the sidebar, the dashboard header, and the final `pl.dashboard(...)` application.

Navigation handlers update the active page state and replace the content children with the selected page.

## Application Pages

The working application currently defines these pages:

- Dashboard
- Analytics
- Forms
- Tables
- Navigation
- Overlays
- Components
- Themes

## Launch Configuration

The working application uses `pl.run(...)` with:

- title: `PyLage UI Kit — Example Application`
- output: `first_app.html`
- serve: `True`
- host: `0.0.0.0`
- port: `3000`

The launch configuration is defined in `working_demo/app.py`.

## API Boundary

Application code imports the public package namespace:

```python
import pylage as pl
```

The working application uses public APIs including `pl.dashboard`, `pl.navigation`, `pl.navigation_item`, `pl.state`, `pl.derived`, `pl.column`, `pl.row`, `pl.form`, `pl.table`, `pl.drawer`, `pl.modal`, `pl.toast`, and `pl.set_theme`.

## Repository Verification

From the repository root, verify the package and working application imports:

```bash
.venv/bin/python -c "import pylage; print('PYLAGE IMPORT: PASS'); print(pylage.__file__)"
.venv/bin/python -c "import working_demo.app as app; print('WORKING DEMO IMPORT: PASS'); print('APP FACTORY:', callable(app.get_app))"
```

The verified development environment successfully imports `pylage` from the repository checkout and imports `working_demo.app` with a callable `get_app` factory.

## Verification

The repository import path and working demo module have been verified with the project Python environment.

Direct execution with `python working_demo/app.py` is not documented as a verified launch method because that execution mode does not preserve the repository import path required by the application.

## Verified Sources

- `working_demo/app.py` — actual working application, page definitions, application factory, and launch configuration.
- `working_demo/__init__.py` — working demo package.
- Repository import-path verification.

## Status

First-app documentation reflects the actual `working_demo/` application and the verified repository import workflow.
