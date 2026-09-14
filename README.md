# PyLage

[![PyPI version](https://img.shields.io/pypi/v/pylage.svg)](https://pypi.org/project/pylage/)
[![Python versions](https://img.shields.io/pypi/pyversions/pylage.svg)](https://pypi.org/project/pylage/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/tests-1332%20passed-brightgreen)](https://github.com/aanalyst-rachit/pylage)
[![GitHub](https://img.shields.io/badge/GitHub-aanalyst--rachit%2Fpylage-blue?logo=github)](https://github.com/aanalyst-rachit/pylage)

**PyLage** is a server-driven differential UI framework for Python.

**Current release: 1.0.4**

Build interactive web applications using pure Python components, reactive state, routing, styling, themes, events, and live browser synchronization — without writing a separate frontend application.

```python
import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading("Hello PyLage"),
    pl.text(count),
    pl.button("Increment", on_click=increment),
)

pl.run(app)
```

## Why PyLage?

PyLage keeps your application logic in Python while delivering a reactive browser UI.

```
Python Application
        │
        ▼
     PyLage
        │
        ├── Components
        ├── Reactive State
        ├── Layout
        ├── Styling & Themes
        ├── Events
        ├── Routing
        └── Differential UI Updates
                │
                ▼
             Browser
```

The browser communicates with the Python runtime over WebSocket. Updates are sent as targeted differential patches instead of full page rebuilds.

## Features

- Python-first UI development
- Server-driven architecture
- Reactive state management
- Differential browser updates
- WebSocket-based live synchronization
- Component-based composition
- Layout primitives (`row`, `column`, etc.)
- Event handling
- Input binding
- Routing & navigation
- Styling API + style overrides
- Light & dark themes
- Responsive support
- Interactive Playground
- CLI support
- Python 3.10+
- Comprehensive test suite + browser verification

## Installation

Requires **Python 3.10+**.

```bash
pip install pylage
```

For development and browser testing:

```bash
pip install "pylage[test]"
```

Core runtime dependencies:
- `websockets >= 10.0`
- `granian >= 2.7.4`
- `msgpack >= 1.0.7`

## Quickstart

```python
import pylage as pl

app = pl.column(
    pl.heading("Hello PyLage"),
    pl.text("A server-driven UI built entirely in Python."),
    pl.button("Click me"),
)

pl.run(app)
```

Import everything from the root package:

```python
import pylage as pl
```

Common public APIs:

```python
pl.column(...)
pl.row(...)
pl.text(...)
pl.heading(...)
pl.button(...)
pl.input(...)
pl.state(...)
pl.style(...)
pl.set_theme(...)
pl.get_current_theme(...)
pl.run(...)
```

## Reactive State

```python
import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading("Counter"),
    pl.text(count),
    pl.button("Increment", on_click=increment),
)

pl.run(app)
```

When state changes, PyLage automatically tracks affected UI and sends only the required differential updates to the browser.

## Components & Layout

```python
import pylage as pl

app = pl.column(
    pl.heading("Dashboard"),
    pl.text("Welcome to PyLage"),
    pl.row(
        pl.button("Save"),
        pl.button("Cancel"),
    ),
)

pl.run(app)
```

Components support nesting, properties, event handlers, reactive values, and recursive layout composition.

## Events

```python
import pylage as pl

message = pl.state("Waiting...")

def save():
    message.set("Saved")

app = pl.column(
    pl.text(message),
    pl.button("Save", on_click=save),
)

pl.run(app)
```

Flow:

```
Browser Event → WebSocket → Python Handler → State Change → Differential Patch → Browser
```

## Inputs & Binding

```python
import pylage as pl

name = pl.state("")

app = pl.column(
    pl.heading("Profile"),
    pl.input(value=name),
    pl.text(name),
)

pl.run(app)
```

## Routing

PyLage includes built-in routing for multi-view applications with navigation, browser history support, and reactive route state — all within the same server-driven model.

## Styling & Themes

```python
import pylage as pl

pl.set_theme("dark")

app = pl.column(
    pl.heading("Styled UI"),
    pl.button(
        "Save",
        style=pl.style(padding="1rem"),
    ),
)

pl.run(app)
```

Inspect the active theme:

```python
pl.get_current_theme()
```

## Architecture

```
Python Application
       │
       ▼
Component Tree
       │
       ▼
Reactive Runtime
       │
       ▼
Differential Update
       │
       ▼
WebSocket
       │
       ▼
Browser
```

Only the necessary changes are transmitted.

## Playground

PyLage ships with a public Playground for interactive exploration of components, reactive behavior, and the public API.

## CLI

```bash
pylage
```

## Development

```bash
git clone https://github.com/aanalyst-rachit/pylage.git
cd pylage

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[test]"
```

### Testing

```bash
# Full suite
pytest

# Browser tests
pytest test/browser -q

# Focused
pytest test/reactive -q
```

Current verification baseline:
- **1333** tests collected
- **1332** passed
- **1** skipped

Additional tooling: Ruff, Playwright, package build verification, dependency auditing.

## Documentation

Documentation lives in `docs/` and is built with MkDocs:

```bash
mkdocs build
```

Key pages:
- `docs/index.md`
- `docs/first_app.md`
- `docs/deployment.md`

## Project Structure

```
pylage/
├── pylage/
│   ├── ENGINE/
│   ├── UI/
│   ├── __init__.py
│   └── cli.py
├── docs/
├── playground/
├── demo/
├── test/
├── scripts/
├── .github/
├── CHANGELOG.md
├── Dockerfile
├── mkdocs.yml
├── pyproject.toml
├── README.md
└── tracker.md
```

## Deployment

See [`docs/deployment.md`](docs/deployment.md) for production server configuration and deployment guidance.

## Release Status

- Current release: **PyLage 1.0.4**
- Release status: **Public release preparation complete**

Release process includes full public API audit, documentation & playground verification, package builds, fresh-install checks, and regression testing.

## License

This project is licensed under the [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

See the [LICENSE](LICENSE) file for the full license text.

## Links

- **Repository:** https://github.com/aanalyst-rachit/pylage
- **PyPI:** https://pypi.org/project/pylage/
- **Issues:** https://github.com/aanalyst-rachit/pylage/issues
- **Playground:** https://aanalyst-rachit.github.io/pylage/playground/
- **Docs:** https://aanalyst-rachit.github.io/pylage/

## Contributing

Contributions, bug reports, and documentation improvements are welcome.

Before submitting:

```bash
pytest
ruff check .
git diff --check
```
