# PyLage
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg?logo=apache&logoColor=white)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Build](https://img.shields.io/badge/Build-Passing-success?logo=github-actions&logoColor=white)](#)
[![Stars](https://img.shields.io/github/stars/aanalyst-rachit/pylage?style=social)](https://github.com/aanalyst-rachit/pylage)

---

PyLage is a reactive, server-driven differential UI framework for Python.

Build web interfaces as Python component trees, connect components to reactive state, and let PyLage render static HTML or synchronize live changes with a browser through its server-driven runtime.

PyLage is designed to keep application UI logic in Python while providing reusable components, reactive updates, styling, theming, layouts, forms, dashboards, feedback components, and browser synchronization.

## Features

* Pure Python UI component model
* Reactive `state` values with dependency tracking
* Server-driven UI updates
* Differential rendering and DOM patching
* Static HTML generation
* Live HTTP and WebSocket applications
* Two-way input binding through reactive state
* Built-in layout components such as `row`, `column`, `stack`, `grid`, `split`, and `container`
* Application and dashboard components
* Navigation, sidebar, drawer, modal, dialog, toast, tooltip, and overlay components
* Forms and input components
* Tables, lists, metrics, cards, and data-oriented components
* Built-in `style` and `theme` APIs
* Light and dark theme support
* Responsive UI primitives
* No frontend build system required for normal PyLage applications
* Stable lowercase public API
* Python 3.10 or newer
* 1090 passing tests in the current release verification suite

## Installation

PyLage 1.0.1 is distributed as a Python package.

```bash
pip install pylage

```

PyLage requires Python 3.10 or newer and depends on:

* `websockets>=10.0`

## Quickstart

A minimal PyLage application can be built directly from Python components.

```python
import pylage as pl

app = pl.column(
    pl.heading("Hello PyLage"),
    pl.text("A server-driven UI built entirely in Python."),
    pl.button("Click me"),
)

pl.run(app)

```

The public API uses lowercase names. Theme control is provided through set_theme and get_current_theme. Examples include column, row, text, heading, button, state, input, and style.

## Reactive State

Reactive state is created with `state`.

```python
import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading(count),
    pl.button("Increment", on_click=increment),
)

pl.run(app)

```

When the state changes, PyLage tracks the affected component properties and updates the browser without requiring the application to rebuild the complete page manually.

## Playground

PyLage includes a live Python-to-UI playground for exploring the framework directly in the browser.

The V1 Playground provides:

* a modern landing page with PyLage product positioning
* a two-pane Python editor and live UI preview
* browser-side Python execution through Pyodide
* installation and execution of the current PyLage wheel in the browser
* examples built from the current V1 `import pylage as pl` API
* reactive component demonstrations
* loading and execution error states
* responsive desktop and mobile behavior
* direct integration with the existing MkDocs documentation
* GitHub Pages deployment for the public Playground

The Playground is a V1 capability and does not require the V2 runtime architecture. It is part of the frozen V1 baseline before V2 development begins.

The reactive pipeline is conceptually:

```text
State
  ↓
Dependency Graph
  ↓
Dirty Nodes
  ↓
Scheduler
  ↓
Component Tree
  ↓
Snapshot / Diff
  ↓
Patch
  ↓
WebSocket
  ↓
Browser DOM

```

Multiple synchronous state changes can be collected by the scheduler and applied as a single update cycle.

## Static and Live Rendering

PyLage can be used for static output as well as live server-driven applications.

Static rendering is useful when an HTML document is sufficient:

```python
pl.run(app, serve=False, output="dist/index.html")

```

For interactive applications, enable the live server mode:

```python
pl.run(app, serve=True)

```

In live mode, browser events are sent to the Python application through the WebSocket connection. Python-side state changes are then converted into differential updates and applied to the browser DOM.

## Two-Way Input Binding

Inputs can be connected directly to reactive state.

```python
import pylage as pl

name = pl.state("PyLage")

app = pl.column(
    pl.heading(name),
    pl.input(value=name),
)

pl.run(app, serve=True)

```

The same state can therefore drive displayed UI and receive changes from browser input events.

## Component Model

PyLage components are Python objects represented as a component tree.

| Category | Examples |
| --- | --- |
| **Basic UI** | `text`, `heading`, `button`, `icon`, `image`, `divider` |
| **Layout** | `container`, `row`, `column`, `stack`, `grid`, `split`, `center` |
| **Navigation** | `navigation`, `navigation_item`, `navbar`, `breadcrumb_trail`, `tabs`, `pagination` |
| **Application shell** | `app_shell`, `top_header`, `topbar`, `sidebar_layout`, `navigation_drawer`, `mobile_sidebar` |
| **Forms** | `form`, `form_field`, `input`, `textarea`, `checkbox`, `radio_group`, `select`, `slider`, `switch`, `datepicker` |
| **Data** | `table`, `data_list`, `dataframe`, `metric`, `metric_card`, `metric_grid`, `stat_group`, `trend` |
| **Dashboard** | `dashboard`, `dashboard_page`, `dashboard_header`, `dashboard_section`, `dashboard_card`, `dashboard_grid` |
| **Feedback** | `alert`, `toast`, `tooltip`, `popover`, `dialog`, `modal`, `confirmation_dialog` |
| **Loading** | `loading`, `loading_state`, `loading_overlay`, `spinner`, `skeleton` |
| **Content sections** | `hero`, `feature_section`, `content_section`, `contact_section`, `cta`, `faq`, `pricing_section`, `testimonial`, `newsletter_section`, `footer` |
| **Media** | `audio`, `video`, `canvas`, `carousel` |
| **Identity** | `avatar`, `badge`, `profile_page`, `authentication` |

The complete public root API is exposed through the `pylage` package.

## Layout

PyLage includes reusable layout primitives for composing interfaces without requiring a separate layout package.

```python
import pylage as pl

app = pl.row(
    pl.column(
        pl.heading("Navigation"),
        pl.button("Home"),
        pl.button("Settings"),
    ),
    pl.column(
        pl.heading("Content"),
        pl.text("Main application content"),
    ),
)

```

Useful layout primitives include:

* `container`
* `row`
* `column`
* `stack`
* `grid`
* `split`
* `center`
* `section`
* `two_column`
* `three_column`

Application-level layouts include:

* `app_shell`
* `top_header`
* `topbar`
* `sidebar_layout`
* `navigation_drawer`
* `mobile_sidebar`

## Styling

PyLage provides a Python styling API through `style`.

```python
import pylage as pl

app = pl.column(
    pl.heading("Styled UI"),
    pl.text("Styles are defined from Python."),
    style=pl.style(
        display="flex",
        flex_direction="column",
    ),
)

```

Styles can be supplied to components and composed with component defaults.
The styling system supports layout properties, typography, spacing, sizing, borders, backgrounds, responsive values, and other UI presentation concerns.

## Themes

PyLage provides a theme API for application-wide visual configuration.

```python
import pylage as pl

pl.set_theme("dark")

```

The current theme can also be accessed through:

```python
pl.get_current_theme()

```

Applications can use the built-in theme system or construct custom theme configurations where required.

## Server-Driven Architecture

PyLage follows a server-driven architecture.

```text
Python Application
       │
       ▼
Component Tree
       │
       ├── Props
       ├── State
       └── Events
       │
       ▼
Reactive Runtime
       │
       ├── Dependency Tracking
       ├── Dirty Node Tracking
       └── Scheduling
       │
       ▼
Snapshot / Differential Update
       │
       ▼
WebSocket Transport
       │
       ▼
Browser Runtime
       │
       ▼
DOM Update

```

The browser does not need to own the application state. Python remains the source of truth while the runtime synchronizes the browser representation.

## Events

Interactive components can receive Python callbacks.

```python
import pylage as pl

count = pl.state(0)

def increment():
    count.set(count.value + 1)

app = pl.column(
    pl.heading(count),
    pl.button("Increment", on_click=increment),
)

pl.run(app, serve=True)

```

The general event path is:

```text
Browser Event
  ↓
WebSocket Event Message
  ↓
Python Event Dispatcher
  ↓
Application Handler
  ↓
State Change
  ↓
Reactive Update
  ↓
Differential Browser Patch

```

## Browser Synchronization

Live PyLage applications use WebSocket communication to synchronize browser events and server-side updates.
The server can update:

* text content
* attributes
* properties
* component structure
* component children
* component ordering
* other supported differential UI state

The browser receives only the changes required by the current update rather than requiring a complete page reload.

## Public API

The stable public API is exposed from the root `pylage` package.
Examples include:

```python
import pylage as pl

pl.button(...)
pl.card(...)
pl.column(...)
pl.container(...)
pl.heading(...)
pl.input(...)
pl.row(...)
pl.state(...)
pl.style(...)
pl.text(...)
pl.run(...)

```

The public API is intentionally lowercase and was stabilized as part of the 1.0 release line.

## Testing

The current PyLage release has a verified test suite covering the public API, components, reactivity, rendering, runtime behavior, styling, themes, events, compatibility, and release checks.

Current verification:

* **1090 passed**

Release verification also covers:

* public API wrappers
* compatibility checks
* import audit
* package metadata
* demo imports
* package build
* wheel installation
* source distribution installation
* clean-environment imports
* release-facing functionality

## Project Structure

The final repository is organized around the current PyLage implementation:

```text
pylage/
├── demo/
├── docs/
├── pylage/
├── scripts/
├── test/
├── working_demo/
├── CHANGELOG.md
├── LICENSE
├── README.md
├── pyproject.toml
└── pytest.ini

```

The repository also contains release and development artifacts used during verification.

## Development

Clone the repository and create a Python 3.10+ virtual environment.

```bash
git clone https://github.com/aanalyst-rachit/pylage.git
cd pylage
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

```

Run the test suite with:

```bash
pytest

```

Run the release verification suite with:

```bash
python3 scripts/verify_release.py

```

## Release

The current release is **PyLage 1.0.1**.

Release metadata is maintained in `pyproject.toml`.
The release history is documented in `CHANGELOG.md`.

## Repository History

The canonical `pylage` repository preserves the development histories of the related PyLage projects that preceded the consolidated release.
The final working tree follows the stabilized `pylage-ui-speed` implementation while preserving the historical Git lineage of:

* PyLage
* pylage-ui
* pylage_layout
* pylage-ui-speed

This preserves historical development context without retaining the obsolete source layouts from those earlier repositories.

## License

PyLage is distributed under the license included in the repository `LICENSE` file.

## Links

* **Repository:** [https://github.com/aanalyst-rachit/pylage](https://github.com/aanalyst-rachit/pylage)
* **Issues:** [https://github.com/aanalyst-rachit/pylage/issues](https://github.com/aanalyst-rachit/pylage/issues)

---
