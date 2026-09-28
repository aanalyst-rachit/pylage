# Routing API

Canonical URI: `/api/routing/`

PyLage routing APIs define routes, resolve page modules, and connect routing to application rendering.

## `pl.route`

Declares or describes a route.

```python
route = pl.route("/dashboard")
```

## `pl.router`

Creates a router for a pages directory or route collection.

```python
router = pl.router("pages")
```

## `pl.routing_runtime`

Creates the runtime integration between a router and the rendered application.

For ordinary applications, prefer `pl.app(...)` and `pl.run(...)`.

## Typical pages setup

```python
import pylage as pl

pl.run(
    pages_dir="pages",
    title="My App",
    serve=True,
)
```

## Related documentation

- [Navigation](../component/navigation.md)
- [API Audit](../helper/api_audit.md)

## Implementation references

- `pylage/ENGINE/routing/`
- `pylage/ENGINE/routing/runtime.py`
