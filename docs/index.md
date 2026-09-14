# PyLage

**Simple, ultrafast, low-latency Python UI**

PyLage is a Python-first, server-driven reactive UI framework. Build interactive web apps with pure Python components, reactive state, routing, themes, and live browser synchronization — without a separate frontend stack.

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

## Why PyLage

- Python-first UI development
- Server-driven reactive UI
- Differential rendering and updates
- Low-latency state updates
- No frontend build system required
- Session-based runtime architecture
- Routing, themes, and production deployment support

## Quick install

```bash
pip install pylage
```

Requires **Python 3.10+**. Current release: **1.0.4**.

## Getting started

1. [Installation](helper/installation.md)
2. [First App](first_app.md)
3. [Deployment](deployment.md)
4. [Playground](https://aanalyst-rachit.github.io/pylage/playground/) (interactive)

## Project

- [GitHub repository](https://github.com/aanalyst-rachit/pylage)
- [Release notes (v1.0.4)](https://github.com/aanalyst-rachit/pylage/releases/tag/v1.0.4)
- [PyPI](https://pypi.org/project/pylage/)
