# PyLage

[![PyPI version](https://img.shields.io/pypi/v/pylage.svg)](https://pypi.org/project/pylage/)
[![Python versions](https://img.shields.io/pypi/pyversions/pylage.svg)](https://pypi.org/project/pylage/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/tests-1435%20passed-brightgreen)](https://github.com/aanalyst-rachit/pylage)
[![GitHub](https://img.shields.io/badge/GitHub-aanalyst--rachit%2Fpylage-blue?logo=github)](https://github.com/aanalyst-rachit/pylage)

**PyLage** is a server-driven differential UI framework for Python.

**Current release: 1.0.6**

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

### Session-Isolated Applications

For served applications that need independent state for each browser session, use `app_factory` with `pl.run(...)`. The factory should create and return a fresh component tree each time it is called.

```python
import pylage as pl


def create_app():
    count = pl.state(0)

    def increment():
        count.set(count.value + 1)

    return pl.column(
        pl.heading("Session Counter"),
        pl.text(count),
        pl.button("Increment", on_click=increment),
    )


if __name__ == "__main__":
    pl.run(
        app_factory=create_app,
        title="Session Counter",
        host="127.0.0.1",
        port=3000,
        serve=True,
    )
```

With `app_factory`, PyLage creates a fresh application/component tree for each new session. Browser sessions therefore keep their reactive state isolated from one another.

The factory must return a new `Component` tree. Application-level persistence, such as users, database records, or data that must survive a page reload, should still be implemented by the application itself using an appropriate persistence layer.

Application code should use the public `pl.run(app_factory=...)` API and should not depend on PyLage private runtime helpers for session creation or component ID management.

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

## Charts

PyLage includes a native chart API for building interactive data visualizations directly from Python. Charts use the optional Plotly dependency and integrate with the same server-driven component model as the rest of the framework.

Install chart support with:

```bash
pip install "pylage[charts]"
```

### Native Data API

Create charts directly from pandas DataFrames, Polars DataFrames, LazyFrames, lists of records, or column mappings:

```python
import pandas as pd
import pylage as pl

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "sales": [120, 180, 150, 220],
})

app = pl.column(
    pl.heading("Sales"),
    pl.chart(
        data=df,
        type="bar",
        x="month",
        y="sales",
    ),
)

pl.run(app)
```

The native API supports:

- `line`
- `bar`
- `scatter`
- `area`
- `pie`
- Multiple `y` columns for supported Cartesian charts
- `color` grouping for supported Cartesian charts
- `size` for scatter charts
- `name`, `x_label`, and `y_label`

### Advanced Plotly API

For full Plotly control, pass an existing Plotly Figure:

```python
import plotly.express as px
import pylage as pl

fig = px.line(
    x=["Jan", "Feb", "Mar"],
    y=[120, 180, 150],
    labels={"x": "Month", "y": "Sales"},
)

app = pl.column(
    pl.heading("Sales Trend"),
    pl.chart(fig),
)

pl.run(app)
```

The advanced Figure API supports Plotly Express and `plotly.graph_objects`, including reactive Figure/state workflows.

Charts also support interactive events such as:

- `on_click`
- `on_select`
- `on_hover`
- `on_relayout`

See the full [Chart documentation](docs/component/chart.md) for installation, supported chart types, events, lifecycle behavior, deployment requirements, browser runtime assets, performance considerations, and troubleshooting.

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

## Benchmark

PyLage includes a reproducible browser-level benchmark comparing PyLage, NiceGUI, Streamlit, and Reflex across counter and form interaction scenarios.

The benchmark uses fresh server processes, fresh Playwright pages, 20 warmup interactions, 50 measured interactions, and DOM-visible completion conditions.

Final benchmark reports and raw samples are available in `pylage-bench/`. The complete methodology and results are documented in the [Benchmark documentation](docs/benchmark.md).

### Final Counter Results

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) |
|---|---:|---:|---:|---:|
| PyLage | 409.48 | 60.61 | 74.33 | 61.36 |
| NiceGUI | 1015.95 | 79.99 | 96.51 | 81.66 |
| Reflex | 709.79 | 61.18 | 68.06 | 61.28 |
| Streamlit | 3329.76 | 255.36 | 316.59 | 259.90 |

### Final Form Results

| Framework | Startup (ms) | P50 (ms) | P95 (ms) | Mean (ms) |
|---|---:|---:|---:|---:|
| PyLage | 597.09 | 116.42 | 129.34 | 115.21 |
| NiceGUI | 1049.05 | 143.04 | 175.01 | 142.95 |
| Reflex | 722.71 | 85.41 | 108.14 | 87.48 |
| Streamlit | 3232.20 | 563.77 | 639.92 | 542.94 |

> These measurements apply to the defined benchmark scenarios and test environment; they should not be interpreted as a universal performance ranking.

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

- Current release: **PyLage 1.0.6**
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
