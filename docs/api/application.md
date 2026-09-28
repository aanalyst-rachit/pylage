# Application API

Canonical URI: `/api/application/`

The application API provides the public entry points for constructing and running PyLage applications.

## `pl.app()`

Creates the public application facade used for page and navigation configuration.

```python
pl.app(pages=None, navigation=None, **kwargs)
```

Use `pl.app()` when an application object is needed. The implementation delegates to the PyLage application layer.

## `pl.run()`

Runs a PyLage application using the public runtime interface.

```python
pl.run(
    app=None,
    *, 
    app_factory=None,
    pages_dir=None,
    title="PyLage App",
    output="index.html",
    serve=False,
    host="127.0.0.1",
    port=0,
    open_browser=True,
    runtime="local",
)
```

Exactly one application source may be supplied: `app`, `app_factory`, or `pages_dir`.

### Application sources

| Argument | Purpose |
| --- | --- |
| `app` | A `Component` root to render. |
| `app_factory` | A callable returning the application root. |
| `pages_dir` | A directory containing routed PyLage pages. |

### Runtime selection

`runtime="local"` preserves the default local PyLage runtime.

`runtime="granian"` selects the embedded Granian ASGI runtime for direct `pl.run()` usage.

```python
import pylage as pl

pl.run(
    pages_dir="pages",
    serve=True,
    runtime="granian",
    host="0.0.0.0",
    port=3010,
)
```

The Granian runtime accepts a `Component` root or `pages_dir` directly. End users do not need to import `ASGIApp` or `EmbeddedGranianRuntime` for this public path.

### Compatibility

The existing `app_factory` serving path remains supported. Invalid runtime values raise `ValueError`, and supplying more than one of `app`, `app_factory`, or `pages_dir` raises `TypeError`.

## `pl.__version__`

Returns the installed PyLage package version.

```python
pl.__version__
```

## Implementation references

- Public facade: `pylage/__init__.py`
- Application runner: `pylage/ENGINE/app.py`
- ASGI application: `pylage/ENGINE/runtime/asgi.py`
- Embedded Granian runtime: `pylage/ENGINE/runtime/granian.py`
