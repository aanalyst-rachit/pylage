# Runtime API

Canonical URI: `/api/runtime/`

Runtime implementation details are normally selected through `pl.run()`. Lower-level runtime classes exist for framework integration and advanced use.

## Recommended public entry point

Use `pl.run(..., runtime="granian")` instead of constructing the Granian runtime manually.

```python
import pylage as pl

pl.run(
    app=my_app,
    serve=True,
    runtime="granian",
    host="0.0.0.0",
    port=3010,
)
```

## `EmbeddedGranianRuntime`

The embedded Granian backend runs a PyLage `ASGIApp` inside the application process.

It is an implementation-level runtime used by `pl.run(runtime="granian")`; most applications should not need to import it directly.

## `ASGIApp`

`ASGIApp` adapts a PyLage component root, application factory, or pages directory to the ASGI interface used by the Granian backend.

The public application API handles this conversion automatically.

## Runtime selection contract

| Runtime | Public usage |
| --- | --- |
| `local` | `pl.run(...)` default |
| `granian` | `pl.run(..., runtime="granian")` |

## Implementation references

- `pylage/ENGINE/runtime/asgi.py`
- `pylage/ENGINE/runtime/granian.py`
- `pylage/ENGINE/runtime/__init__.py`
- `pylage/ENGINE/app.py`
