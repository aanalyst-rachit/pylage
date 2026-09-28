# PyLage

---

[![PyPI version](https://img.shields.io/pypi/v/pylage.svg)](https://pypi.org/project/pylage/)
[![Python versions](https://img.shields.io/pypi/pyversions/pylage.svg)](https://pypi.org/project/pylage/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Tests](https://img.shields.io/badge/tests-1537%20passed-brightgreen)](https://github.com/aanalyst-rachit/pylage)
[![GitHub](https://img.shields.io/badge/GitHub-aanalyst--rachit%2Fpylage-blue?logo=github)](https://github.com/aanalyst-rachit/pylage)

---

**PyLage** is a Python-first framework for building reactive web interfaces with components, state, routing, layouts, forms, navigation, dashboards, charts, themes, and application-level page patterns.

**Current release:** `1.0.7`

PyLage is designed around a simple idea:

```python
import pylage as pl

count = pl.state(0)

app = pl.column(
    pl.heading("Counter"),
    pl.text(count),
    pl.button("Increment", on_click=lambda: count.set(count.value + 1)),
)

pl.run(app)
```

---

## Why PyLage?

* Python-first UI development
* Reactive state and derived state
* Composable components
* Built-in layouts and page patterns
* Forms and input components
* Navigation and Drawer components
* File-system routing
* Charts and data components
* Themes and styling
* Local development server
* Production-oriented serving options
* Public API available directly from `pylage`

The recommended application style is:

```python
import pylage as pl
```

PyLage's internal `ENGINE` and `UI` packages are implementation details and should not be required by application code.

---

## Installation

Install the released package:

```bash
pip install pylage
```

Then create an application:

```python
import pylage as pl

app = pl.column(
    pl.heading("Hello, PyLage"),
    pl.text("My first PyLage application."),
)

pl.run(app)
```

---

# Quickstart

A minimal application:

```python
import pylage as pl

app = pl.column(
    pl.heading("Welcome"),
    pl.text("Built with PyLage."),
    pl.button("Get Started"),
)

pl.run(app)
```

A reactive application:

```python
import pylage as pl

count = pl.state(0)

app = pl.column(
    pl.heading("Counter"),
    pl.text(count),
    pl.button(
        "Increment",
        on_click=lambda: count.set(count.value + 1),
    ),
)

pl.run(app)
```

A complete application can also be split into pages and launched through the router:

```python
import pylage as pl

pl.run(
    pages_dir="pages",
    title="My PyLage App",
    serve=True,
    port=3000,
)
```

---

# Core Concepts

## State

`state()` creates reactive state.

```python
import pylage as pl

name = pl.state("PyLage")

app = pl.column(
    pl.heading("Hello"),
    pl.text(name),
)
```

State can be changed from event handlers:

```python
count = pl.state(0)

pl.button(
    "Increment",
    on_click=lambda: count.set(count.value + 1),
)
```

---

## Derived State

Use `derived()` when a value depends on other state values.

```python
import pylage as pl

first = pl.state("Py")
second = pl.state("Lage")

full_name = pl.derived(
    first,
    second,
    compute=lambda a, b: a + b,
)

app = pl.column(
    pl.text(first),
    pl.text(second),
    pl.heading(full_name),
)
```

---

## Conditional Rendering

`cond()` selects between two branches using reactive state.

```python
import pylage as pl

logged_in = pl.state(False)

app = pl.column(
    pl.button(
        "Toggle",
        on_click=lambda: logged_in.set(not logged_in.value),
    ),
    pl.cond(
        logged_in,
        pl.text("Welcome back!"),
        pl.text("Please sign in."),
    ),
)
```

---

## Reactive Lists

`reactive_list()` creates a reactive collection.

```python
import pylage as pl

items = pl.reactive_list(["Python", "PyLage", "Web"])
```

Render the collection with `for_each()`:

```python
app = pl.column(
    pl.for_each(
        items,
        lambda item: pl.text(item),
    ),
)
```

---

# Layout

PyLage provides several composable layout primitives.

## Column

```python
pl.column(
    pl.heading("Column"),
    pl.text("Item one"),
    pl.text("Item two"),
)
```

## Row

```python
pl.row(
    pl.button("Save"),
    pl.button("Cancel"),
)
```

## Stack

```python
pl.stack(
    pl.text("Background"),
    pl.button("Action"),
)
```

## Grid

```python
pl.grid(
    pl.card(pl.text("One")),
    pl.card(pl.text("Two")),
    pl.card(pl.text("Three")),
)
```

## Center

```python
pl.center(
    pl.heading("Centered content"),
)
```

## Container

```python
pl.container(
    pl.heading("Content"),
    pl.text("Contained content"),
)
```

## Section

```python
pl.section(
    pl.heading("Section"),
    pl.text("Section content"),
)
```

## Split

```python
pl.split(
    pl.column(pl.heading("Left")),
    pl.column(pl.heading("Right")),
)
```

## Two Column

```python
pl.two_column(
    pl.card(pl.text("Left")),
    pl.card(pl.text("Right")),
)
```

## Three Column

```python
pl.three_column(
    pl.card(pl.text("One")),
    pl.card(pl.text("Two")),
    pl.card(pl.text("Three")),
)
```

---

# Basic UI Components

## Text

```python
pl.text("Hello PyLage")
pl.text("Muted text", muted=True)
pl.text("Caption", caption=True)
```

## Heading

```python
pl.heading("Dashboard")
```

## Card

```python
pl.card(
    heading="Profile",
    body=pl.text("User information"),
    footer=pl.button("Edit"),
)
```

Cards can also be composed:

```python
pl.card(
    pl.heading("Card title"),
    pl.text("Card content"),
)
```

## Badge

```python
pl.badge("Active")
pl.badge("Warning", variant="warning")
```

## Avatar

```python
pl.avatar(
    pl.image(src="/avatar.png", alt="User"),
)
```

## Icon

```python
pl.icon(name="home")
```

## Image

```python
pl.image(
    src="/images/hero.png",
    alt="PyLage application",
)
```

## Divider

```python
pl.divider()
```

## List

```python
pl.list(
    "Python",
    "PyLage",
    "Reactive UI",
)
```

## Menu

```python
pl.menu(
    pl.navigation_item("Home"),
    pl.navigation_item("Settings"),
)
```

---

# Buttons and Links

## Button

```python
pl.button("Save")
```

Variants and sizes can be specified:

```python
pl.button(
    "Delete",
    variant="danger",
    size="sm",
)
```

## Link

```python
pl.link(
    "Documentation",
    href="/docs",
)
```

---

# Forms & Inputs

## Input

```python
name = pl.state("")

pl.input(
    value=name,
    placeholder="Your name",
)
```

## Textarea

```python
pl.textarea(
    value="",
    placeholder="Write something...",
)
```

## Checkbox

```python
pl.checkbox(
    value=False,
    label="Accept terms",
)
```

## Switch

```python
pl.switch(
    value=False,
    label="Enable notifications",
)
```

## Select

```python
pl.select(
    pl.option("Python", value="python"),
    pl.option("JavaScript", value="javascript"),
    pl.option("Rust", value="rust"),
)
```

## Option

```python
pl.option("Python", value="python")
```

## Radio Group

```python
pl.radio_group(
    pl.option("Small", value="sm"),
    pl.option("Medium", value="md"),
    pl.option("Large", value="lg"),
)
```

## Slider

```python
pl.slider(
    value=50,
    min=0,
    max=100,
)
```

## Datepicker

```python
pl.datepicker()
```

## Form Field

Wrap an input with a label and validation information:

```python
pl.form_field(
    pl.input(),
    label="Username",
    help_text="Choose a unique username.",
    required=True,
)
```

## Form

```python
pl.form(
    pl.form_field(
        pl.input(),
        label="Name",
        required=True,
    ),
    pl.form_field(
        pl.input(input_type="email"),
        label="Email",
        required=True,
    ),
    pl.button("Submit"),
)
```

## Search Bar

```python
pl.search_bar(
    placeholder="Search projects...",
    button_text="Search",
)
```

---

# Feedback, Dialogs & Overlays

## Alert

```python
pl.alert(
    "Your changes were saved.",
    variant="success",
)
```

## Toast

```python
pl.toast(
    "Saved successfully.",
    variant="success",
)
```

## Modal

```python
pl.modal(
    pl.text("Modal content"),
    open=True,
    title="Example Modal",
)
```

## Dialog

```python
pl.dialog(
    pl.heading("Dialog"),
    pl.text("Dialog content"),
)
```

## Confirmation Dialog

```python
pl.confirmation_dialog(
    "Delete this item?",
    title="Confirm deletion",
    open=True,
    confirm_text="Delete",
    cancel_text="Cancel",
)
```

## Popover

```python
pl.popover(
    pl.button("Open details"),
    pl.text("Additional information"),
)
```

## Tooltip

```python
pl.tooltip(
    pl.button("Help"),
)
```

## Loading

```python
pl.loading()
```

Custom loading text:

```python
pl.loading("Loading projects...")
```

## Loading State

```python
pl.loading_state(
    "Loading dashboard...",
    description="Fetching the latest data.",
)
```

## Loading Overlay

```python
pl.loading_overlay(
    "Saving...",
    open=True,
)
```

## Spinner

```python
pl.spinner()
```

## Skeleton

```python
pl.skeleton()
```

## Empty State

```python
pl.empty_state(
    "No projects",
    "Create a project to get started.",
)
```

## Error State

```python
pl.error_state(
    "Unable to load projects",
    "Please try again.",
)
```

## Progress Bar

```python
pl.progress_bar(value=65)
```

---

# Navigation

## Navigation

```python
pl.navigation(
    pl.navigation_item("Home", current_path="/"),
    pl.navigation_item("Projects", current_path="/projects"),
    pl.navigation_item("Settings", current_path="/settings"),
)
```

## Navigation Item

```python
pl.navigation_item(
    "Dashboard",
    active=True,
)
```

With a path:

```python
pl.navigation_item(
    "Projects",
    current_path="/projects",
)
```

With reactive routing state:

```python
current_path = pl.state("/dashboard")

pl.navigation_item(
    "Dashboard",
    current_path=current_path,
)
```

## Navigation Controls

```python
pl.navigation_controls(
    on_prev=lambda: None,
    on_next=lambda: None,
)
```

## Navbar

```python
pl.navbar(
    pl.link("Home", href="/"),
    pl.link("Projects", href="/projects"),
)
```

## Topbar

```python
pl.topbar(
    pl.heading("My Application"),
)
```

## Top Header

```python
pl.top_header(
    pl.heading("Dashboard"),
)
```

## Breadcrumb Trail

```python
pl.breadcrumb_trail(
    pl.link("Home", href="/"),
    pl.link("Projects", href="/projects"),
    current_path="/projects",
)
```

## Sidebar Layout

```python
pl.sidebar_layout(
    sidebar=pl.navigation(
        pl.navigation_item("Home", current_path="/"),
        pl.navigation_item("Projects", current_path="/projects"),
    ),
    content=pl.text("Page content"),
)
```

---

# Drawer Navigation

PyLage provides three public Drawer-oriented APIs.

## Drawer

```python
pl.drawer(
    pl.heading("Menu"),
    pl.navigation_item("Home"),
    pl.navigation_item("Projects"),
)
```

## Navigation Drawer

```python
pl.navigation_drawer(
    pl.navigation_item("Dashboard"),
    pl.navigation_item("Projects"),
    pl.navigation_item("Settings"),
)
```

## Mobile Sidebar

```python
pl.mobile_sidebar(
    pl.navigation_item("Home"),
    pl.navigation_item("Projects"),
    responsive_mode={
        "base": "overlay",
        "md": "persistent",
    },
)
```

A Drawer can contain arbitrary PyLage content:

```python
pl.drawer(
    pl.heading("Workspace"),
    pl.text("Navigation"),
    pl.button("New project"),
)
```

The same public components can therefore be used for both application navigation and custom side panels.

---

# Pagination

```python
pl.pagination(
    pl.button("Previous"),
    pl.text("Page 2"),
    pl.button("Next"),
)
```

---

# Tables & Data

## Table

```python
pl.table(
    [
        ["Alice", "Admin"],
        ["Bob", "Developer"],
    ],
    headers=["Name", "Role"],
)
```

## Dataframe

```python
pl.dataframe(
    [
        ["Alice", 10],
        ["Bob", 20],
    ],
    headers=["Name", "Score"],
)
```

## Data List

```python
pl.data_list(
    [
        ("Name", "Alice"),
        ("Role", "Developer"),
        ("Status", "Active"),
    ],
)
```

---

# Charts

PyLage exposes both `Chart` and the lowercase `chart` API.

## Chart

```python
pl.Chart(
    data=[
        {"month": "Jan", "sales": 100},
        {"month": "Feb", "sales": 140},
        {"month": "Mar", "sales": 180},
    ],
    type="line",
    x="month",
    y="sales",
    title="Monthly Sales",
)
```

## chart

```python
pl.chart(
    data=[
        {"month": "Jan", "sales": 100},
        {"month": "Feb", "sales": 140},
        {"month": "Mar", "sales": 180},
    ],
    type="bar",
    x="month",
    y="sales",
)
```

Charts can also receive an existing figure:

```python
figure = ...

pl.Chart(
    figure=figure,
    title="Existing Figure",
)
```

---

# Metrics & Statistics

## Metric

```python
pl.metric(
    "Revenue",
    "$24,500",
    delta="+12%",
)
```

## Metric Card

```python
pl.metric_card(
    "Users",
    "12,480",
    delta="+8%",
)
```

## Metric Grid

```python
pl.metric_grid(
    pl.metric("Users", "12,480"),
    pl.metric("Revenue", "$24K"),
    pl.metric("Orders", "842"),
)
```

## Stat Group

```python
pl.stat_group(
    pl.metric("Users", "12K"),
    pl.metric("Orders", "842"),
    pl.metric("Revenue", "$24K"),
)
```

## Stats Section

```python
pl.stats_section(
    title="Overview",
    stats=(
        pl.metric("Users", "12K"),
        pl.metric("Orders", "842"),
    ),
)
```

## Trend

```python
pl.trend(
    12.5,
    direction="up",
)
```

---

# Dashboard Components

## Dashboard Card

```python
pl.dashboard_card(
    title="Revenue",
    body=pl.metric("Revenue", "$24K"),
)
```

## Dashboard Grid

```python
pl.dashboard_grid(
    pl.dashboard_card(title="Users", body=pl.text("12K")),
    pl.dashboard_card(title="Orders", body=pl.text("842")),
)
```

## Dashboard Header

```python
pl.dashboard_header(
    "Analytics",
    "Business performance overview",
)
```

## Dashboard Section

```python
pl.dashboard_section(
    pl.metric("Revenue", "$24K"),
    title="Revenue",
    description="Current monthly revenue.",
)
```

## Dashboard

```python
pl.dashboard(
    title="Analytics",
    content=pl.dashboard_grid(
        pl.dashboard_card(
            title="Users",
            body=pl.text("12,480"),
        ),
        pl.dashboard_card(
            title="Revenue",
            body=pl.text("$24K"),
        ),
    ),
)
```

## Dashboard Page

```python
pl.dashboard_page(
    title="Dashboard",
    header=pl.dashboard_header("Overview"),
    content=pl.dashboard_grid(
        pl.dashboard_card(
            title="Revenue",
            body=pl.text("$24K"),
        ),
    ),
)
```

---

# Application & Page Patterns

PyLage includes higher-level page-building components.

## App Shell

```python
pl.app_shell(
    header=pl.top_header(
        pl.heading("My App"),
    ),
    sidebar=pl.navigation(
        pl.navigation_item("Home"),
        pl.navigation_item("Settings"),
    ),
    content=pl.text("Main content"),
    footer=pl.footer(
        pl.text("© My App"),
    ),
)
```

## Hero

```python
pl.hero(
    "Build with Python",
    "Create reactive web applications with PyLage.",
    actions=pl.button("Get Started"),
)
```

## Feature Section

```python
pl.feature_section(
    pl.card(pl.heading("Reactive")),
    pl.card(pl.heading("Composable")),
    title="Features",
)
```

## Content Section

```python
pl.content_section(
    "About PyLage",
    content=pl.text(
        "A Python-first reactive web framework."
    ),
)
```

## CTA

```python
pl.cta(
    "Ready to build?",
    "Start your next application with PyLage.",
    actions=pl.button("Get Started"),
)
```

## Landing Page

```python
pl.landing_page(
    hero=pl.hero(
        "PyLage",
        "Python-first reactive web applications.",
    ),
    features=pl.feature_section(
        pl.card(pl.text("Reactive state")),
        pl.card(pl.text("Composable UI")),
    ),
    cta=pl.cta(
        "Start building",
        actions=pl.button("Get Started"),
    ),
)
```

## Pricing Section

```python
pl.pricing_section()
```

## Profile Page

```python
pl.profile_page(
    name="Rachit",
    role="Developer",
    email="user@example.com",
)
```

## Contact Section

```python
pl.contact_section(
    title="Contact Us",
    description="Send us a message.",
)
```

## Newsletter Section

```python
pl.newsletter_section(
    title="Stay Updated",
    description="Get the latest PyLage updates.",
)
```

## FAQ

```python
pl.faq()
```

## Testimonial

```python
pl.testimonial(
    "PyLage makes Python UI composition simple.",
    "Developer",
    role="Engineer",
)
```

## Admin Panel

```python
pl.admin_panel(
    title="Admin",
    sidebar=pl.navigation(
        pl.navigation_item("Users"),
        pl.navigation_item("Settings"),
    ),
    content=pl.text("Administration"),
)
```

## Authentication

```python
pl.authentication(
    title="Welcome back",
    description="Sign in to continue.",
)
```

---

# Media & Interactive Components

## Audio

```python
pl.audio(
    src="/media/example.mp3",
)
```

## Video

```python
pl.video(
    src="/media/example.mp4",
)
```

## Canvas

```python
pl.canvas(
    width=800,
    height=400,
)
```

## Carousel

```python
pl.carousel(
    pl.image(src="/images/one.png", alt="One"),
    pl.image(src="/images/two.png", alt="Two"),
)
```

## Tabs

```python
pl.tabs(
    pl.text("Overview"),
    pl.text("Activity"),
    pl.text("Settings"),
)
```

## Accordion

```python
pl.accordion(
    pl.heading("Frequently Asked Question"),
    pl.text("Answer"),
)
```

---

# Styling

## style

Use `style()` to create reusable style definitions.

```python
card_style = pl.style(
    padding="1rem",
    border_radius="12px",
)

app = pl.card(
    pl.text("Styled card"),
    style=card_style,
)
```

Inline style properties can also be passed directly:

```python
pl.text(
    "Styled text",
    style=pl.style(
        font_weight="bold",
        padding="0.5rem",
    ),
)
```

---

# Themes

## theme

`theme` is part of PyLage's public theme API.

```python
import pylage as pl

current_theme = pl.theme
```

## colors

The public `colors` API provides the framework's color definitions.

```python
import pylage as pl

palette = pl.colors
```

Use theme-aware styling instead of depending on internal implementation details.

## set_theme

```python
pl.set_theme("dark")
```

A theme object can also be supplied:

```python
theme = pl.theme
pl.set_theme(theme)
```

## get_current_theme

```python
current = pl.get_current_theme()
```

---

# Routing

PyLage supports file-system based routing.

A typical application structure is:

```text
pages/
├── index.py
├── dashboard.py
├── projects.py
└── settings.py
```

A page can be a normal PyLage component tree:

```python
import pylage as pl

page = pl.column(
    pl.heading("Projects"),
    pl.text("Project list"),
)
```

## router

Create a router from a pages directory:

```python
router = pl.router("pages")
```

## route

A route can be represented explicitly:

```python
from pathlib import Path
import pylage as pl

pl.route(
    "/projects",
    Path("pages/projects.py"),
    label="Projects",
)
```

## routing_runtime

Connect routing to a root component:

```python
import pylage as pl

router = pl.router("pages")

root = pl.app_shell(
    header=pl.top_header(
        pl.heading("My Application"),
    ),
    content=pl.container(),
)

pl.routing_runtime(
    router,
    root,
)
```

## app

The public `app()` API provides application-level composition:

```python
import pylage as pl

application = pl.app(
    pages="pages",
)
```

The application can then be passed to `run()`:

```python
pl.run(application)
```

For a file-system routed application, `run()` can also configure the pages directory directly.

---

# Running Applications

## run

Run a component tree:

```python
import pylage as pl

app = pl.column(
    pl.heading("Hello"),
    pl.text("Running locally."),
)

pl.run(app)
```

Run an application factory:

```python
pl.run(
    app_factory=lambda: pl.column(
        pl.heading("New session"),
    ),
)
```

Run a pages directory:

```python
pl.run(
    pages_dir="pages",
    title="PyLage Application",
)
```

Start a development server:

```python
pl.run(
    pages_dir="pages",
    title="PyLage Application",
    serve=True,
    host="127.0.0.1",
    port=3000,
)
```

For a production-oriented runtime:

```python
pl.run(
    pages_dir="pages",
    serve=True,
    host="0.0.0.0",
    port=3000,
    runtime="granian",
)
```

---

# Complete Example

The following example combines state, layout, navigation, forms, metrics, and a table.

```python
import pylage as pl

name = pl.state("")
tasks = pl.reactive_list([
    "Review documentation",
    "Build dashboard",
    "Run tests",
])

app = pl.app_shell(
    header=pl.top_header(
        pl.row(
            pl.heading("Project Dashboard"),
            pl.navigation(
                pl.navigation_item("Dashboard", active=True),
                pl.navigation_item("Projects"),
                pl.navigation_item("Settings"),
            ),
        ),
    ),

    sidebar=pl.navigation_drawer(
        pl.navigation_item("Overview"),
        pl.navigation_item("Projects"),
        pl.navigation_item("Settings"),
    ),

    content=pl.container(
        pl.column(
            pl.heading("Welcome"),
            pl.text(name),

            pl.form(
                pl.form_field(
                    pl.input(
                        value=name,
                        placeholder="Your name",
                    ),
                    label="Name",
                    required=True,
                ),
                pl.button("Save"),
            ),

            pl.metric_grid(
                pl.metric("Projects", "24"),
                pl.metric("Tasks", "142"),
                pl.metric("Progress", "78%"),
            ),

            pl.dashboard_section(
                pl.heading("Tasks"),
                pl.for_each(
                    tasks,
                    lambda task: pl.card(
                        pl.text(task),
                    ),
                ),
                title="Current Tasks",
            ),
        ),
    ),

    footer=pl.footer(
        pl.text("Built with PyLage"),
    ),
)

pl.run(app)
```

---

# Public API Cookbook

The following index covers the complete public API exported from the root `pylage` package.

| Public API            | Example                                          |
| --------------------- | ------------------------------------------------ |
| `Chart`               | `pl.Chart(data=data, type="line")`               |
| `__version__`         | `pl.__version__`                                 |
| `app`                 | `pl.app(pages="pages")`                          |
| `accordion`           | `pl.accordion(pl.text("Content"))`               |
| `admin_panel`         | `pl.admin_panel(title="Admin")`                  |
| `alert`               | `pl.alert("Saved", variant="success")`           |
| `app_shell`           | `pl.app_shell(content=pl.text("Content"))`       |
| `audio`               | `pl.audio(src="/media/example.mp3")`             |
| `authentication`      | `pl.authentication()`                            |
| `avatar`              | `pl.avatar(pl.image(src="/avatar.png"))`         |
| `badge`               | `pl.badge("Active")`                             |
| `breadcrumb_trail`    | `pl.breadcrumb_trail(...)`                       |
| `button`              | `pl.button("Save")`                              |
| `canvas`              | `pl.canvas(width=800, height=400)`               |
| `card`                | `pl.card(pl.text("Content"))`                    |
| `carousel`            | `pl.carousel(...)`                               |
| `center`              | `pl.center(pl.text("Centered"))`                 |
| `chart`               | `pl.chart(data=data, type="bar")`                |
| `checkbox`            | `pl.checkbox(value=False)`                       |
| `colors`              | `pl.colors`                                      |
| `column`              | `pl.column(...)`                                 |
| `cond`                | `pl.cond(condition, true_branch, false_branch)`  |
| `confirmation_dialog` | `pl.confirmation_dialog("Delete?")`              |
| `contact_section`     | `pl.contact_section()`                           |
| `container`           | `pl.container(...)`                              |
| `content_section`     | `pl.content_section("About", content=...)`       |
| `cta`                 | `pl.cta("Get started")`                          |
| `dashboard`           | `pl.dashboard(title="Dashboard")`                |
| `dashboard_card`      | `pl.dashboard_card(title="Users")`               |
| `dashboard_grid`      | `pl.dashboard_grid(...)`                         |
| `dashboard_header`    | `pl.dashboard_header("Dashboard")`               |
| `dashboard_page`      | `pl.dashboard_page(title="Dashboard")`           |
| `dashboard_section`   | `pl.dashboard_section(..., title="Stats")`       |
| `data_list`           | `pl.data_list(data)`                             |
| `dataframe`           | `pl.dataframe(data)`                             |
| `datepicker`          | `pl.datepicker()`                                |
| `derived`             | `pl.derived(a, b, compute=lambda x, y: x + y)`   |
| `dialog`              | `pl.dialog(pl.text("Dialog"))`                   |
| `divider`             | `pl.divider()`                                   |
| `drawer`              | `pl.drawer(...)`                                 |
| `empty_state`         | `pl.empty_state("Nothing here")`                 |
| `error_state`         | `pl.error_state("Something went wrong")`         |
| `faq`                 | `pl.faq()`                                       |
| `feature_section`     | `pl.feature_section(...)`                        |
| `footer`              | `pl.footer(...)`                                 |
| `for_each`            | `pl.for_each(items, render_item)`                |
| `form`                | `pl.form(...)`                                   |
| `form_field`          | `pl.form_field(pl.input(), label="Name")`        |
| `get_current_theme`   | `pl.get_current_theme()`                         |
| `grid`                | `pl.grid(...)`                                   |
| `header`              | `pl.header(...)`                                 |
| `heading`             | `pl.heading("Title")`                            |
| `hero`                | `pl.hero("Title")`                               |
| `icon`                | `pl.icon(name="home")`                           |
| `image`               | `pl.image(src="/image.png", alt="Image")`        |
| `input`               | `pl.input()`                                     |
| `landing_page`        | `pl.landing_page(...)`                           |
| `link`                | `pl.link("Home", href="/")`                      |
| `list`                | `pl.list("One", "Two")`                          |
| `loading`             | `pl.loading()`                                   |
| `loading_overlay`     | `pl.loading_overlay(open=True)`                  |
| `loading_state`       | `pl.loading_state()`                             |
| `menu`                | `pl.menu(...)`                                   |
| `metric`              | `pl.metric("Users", "100")`                      |
| `metric_card`         | `pl.metric_card("Users", "100")`                 |
| `metric_grid`         | `pl.metric_grid(...)`                            |
| `mobile_sidebar`      | `pl.mobile_sidebar(...)`                         |
| `modal`               | `pl.modal(pl.text("Content"))`                   |
| `navbar`              | `pl.navbar(...)`                                 |
| `navigation`          | `pl.navigation(...)`                             |
| `navigation_controls` | `pl.navigation_controls(...)`                    |
| `navigation_drawer`   | `pl.navigation_drawer(...)`                      |
| `navigation_item`     | `pl.navigation_item("Home")`                     |
| `newsletter_section`  | `pl.newsletter_section()`                        |
| `option`              | `pl.option("Python", value="python")`            |
| `pagination`          | `pl.pagination(...)`                             |
| `popover`             | `pl.popover(...)`                                |
| `pricing_section`     | `pl.pricing_section()`                           |
| `profile_page`        | `pl.profile_page(name="Rachit")`                 |
| `progress_bar`        | `pl.progress_bar(value=50)`                      |
| `radio_group`         | `pl.radio_group(...)`                            |
| `reactive_list`       | `pl.reactive_list(["A", "B"])`                   |
| `route`               | `pl.route("/about", source, label="About")`      |
| `router`              | `pl.router("pages")`                             |
| `routing_runtime`     | `pl.routing_runtime(router, root)`               |
| `row`                 | `pl.row(...)`                                    |
| `run`                 | `pl.run(app)`                                    |
| `search_bar`          | `pl.search_bar()`                                |
| `section`             | `pl.section(...)`                                |
| `select`              | `pl.select(pl.option("Python"))`                 |
| `set_theme`           | `pl.set_theme("dark")`                           |
| `sidebar_layout`      | `pl.sidebar_layout(...)`                         |
| `skeleton`            | `pl.skeleton()`                                  |
| `slider`              | `pl.slider()`                                    |
| `spinner`             | `pl.spinner()`                                   |
| `split`               | `pl.split(...)`                                  |
| `stack`               | `pl.stack(...)`                                  |
| `stat_group`          | `pl.stat_group(...)`                             |
| `state`               | `pl.state(0)`                                    |
| `stats_section`       | `pl.stats_section(...)`                          |
| `style`               | `pl.style(padding="1rem")`                       |
| `switch`              | `pl.switch()`                                    |
| `table`               | `pl.table(data)`                                 |
| `tabs`                | `pl.tabs(...)`                                   |
| `testimonial`         | `pl.testimonial("Great framework", "Developer")` |
| `text`                | `pl.text("Hello")`                               |
| `textarea`            | `pl.textarea()`                                  |
| `theme`               | `pl.theme`                                       |
| `three_column`        | `pl.three_column(...)`                           |
| `toast`               | `pl.toast("Saved")`                              |
| `tooltip`             | `pl.tooltip(pl.button("Help"))`                  |
| `top_header`          | `pl.top_header(...)`                             |
| `topbar`              | `pl.topbar(...)`                                 |
| `trend`               | `pl.trend(12.5, direction="up")`                 |
| `two_column`          | `pl.two_column(...)`                             |
| `video`               | `pl.video(src="/media/example.mp4")`             |

---

# Session-Isolated Applications

For applications where each session should receive a fresh component tree, use `app_factory`.

```python
import pylage as pl

def create_app():
    count = pl.state(0)

    return pl.column(
        pl.heading("Session Counter"),
        pl.text(count),
        pl.button(
            "Increment",
            on_click=lambda: count.set(count.value + 1),
        ),
    )

pl.run(
    app_factory=create_app,
    serve=True,
)
```

This keeps application state isolated per created application instance.

---

# CLI & Development

PyLage applications can be run directly from Python:

```bash
python app.py
```

For a pages-based application:

```python
pl.run(
    pages_dir="pages",
    serve=True,
    host="127.0.0.1",
    port=3000,
)
```

For development, keep the application code under normal Python modules and use the public `pylage` API.

---

# Testing

Run the complete test suite with:

```bash
.venv/bin/python -m pytest -q
```

A focused test file can be run with:

```bash
.venv/bin/python -m pytest -q test/path/to/test_file.py
```

Useful final checks:

```bash
.venv/bin/python -m pytest -q
git diff --check
git status --short
```

The latest completed full regression in the v1.0.7 development cycle reached **1,537 passing tests**.

---

# Documentation

PyLage documentation is organized around the public framework surface.

Important component documentation includes:

```text
docs/
├── component/
│   ├── drawer.md
│   └── navigation_item.md
├── benchmark.md
└── releases/
    └── tracker_v1.0.7.md
```

The public API should be preferred over internal implementation modules when writing applications or examples.

---

# Benchmark

PyLage includes browser-level comparative benchmarks covering representative application scenarios.

The benchmark compares PyLage with other Python web UI frameworks under the same test methodology.

The current benchmark documentation covers:

* Counter
* Form
* startup timing
* interaction latency
* P50 latency
* P95 latency
* mean latency

Example benchmark results from the documented browser benchmark:

| Framework | Counter startup | Counter P50 | Counter P95 |
| --------- | --------------: | ----------: | ----------: |
| PyLage    |       409.48 ms |    60.61 ms |    74.33 ms |
| NiceGUI   |      1015.95 ms |    79.99 ms |    96.51 ms |
| Reflex    |       709.79 ms |    61.18 ms |    68.06 ms |
| Streamlit |      3329.76 ms |   255.36 ms |   316.59 ms |

Form scenario:

| Framework | Form startup |  Form P50 |  Form P95 |
| --------- | -----------: | --------: | --------: |
| PyLage    |    597.09 ms | 116.42 ms | 129.34 ms |
| NiceGUI   |   1049.05 ms | 143.04 ms | 175.01 ms |
| Reflex    |    722.71 ms |  85.41 ms | 108.14 ms |
| Streamlit |   3232.20 ms | 563.77 ms | 639.92 ms |

These measurements describe the tested environments and scenarios. They should not be interpreted as universal performance rankings.

---

# Project Structure

A typical PyLage project can be organized as:

```text
pylage-project/
├── app.py
├── pages/
│   ├── index.py
│   ├── dashboard.py
│   ├── projects.py
│   └── settings.py
├── tests/
├── docs/
└── pyproject.toml
```

The framework itself contains the implementation and public API layers, but application code should normally import from:

```python
import pylage as pl
```

---

# Deployment

For a served application:

```python
import pylage as pl

pl.run(
    pages_dir="pages",
    title="Production App",
    serve=True,
    host="0.0.0.0",
    port=3000,
)
```

The `runtime` option can be selected when the deployment environment calls for a different serving runtime:

```python
pl.run(
    pages_dir="pages",
    serve=True,
    runtime="granian",
)
```

Production deployments should use the deployment process appropriate to the target infrastructure.

---

# Release Status

**PyLage 1.0.7 is the current release.**

The release includes the finalized public Drawer/navigation work, routing and runtime improvements, accessibility behavior, responsive behavior, live showcase coverage, documentation, and comprehensive testing completed during the v1.0.7 development cycle.

---

# Contributing

Contributions should:

1. Preserve the public API.
2. Prefer public `pylage` imports in examples.
3. Include tests for behavior changes.
4. Keep documentation synchronized with public APIs.
5. Run the relevant focused tests.
6. Run the complete regression suite before release.
7. Check formatting and repository state before committing.

Recommended final validation:

```bash
.venv/bin/python -m pytest -q
git diff --check
git status --short
```

---

# License

PyLage is distributed under the project's configured license. See the repository license file for the authoritative terms.


# Links

- **Repository:** [GitHub](https://github.com/aanalyst-rachit/pylage)
- **PyPI:** [PyPI](https://pypi.org/project/pylage/)
- **Issues:** [GitHub Issues](https://github.com/aanalyst-rachit/pylage/issues)
- **Playground:** [Live Playground](https://aanalyst-rachit.github.io/pylage/playground/)
- **Docs:** [PyLage Documentation](https://aanalyst-rachit.github.io/pylage/)
git diff --check
```
