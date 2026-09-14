# PyLage v1.0.5 Release Tracker

## Purpose

v1.0.5 records the session-isolation and app-factory runtime improvements made after the v1.0.4 baseline.

## Session-Isolated App Factory

### Problem

Applications using `pl.run(app_factory=...)` could create fresh component trees whose generated component IDs did not match the component IDs used by the initially rendered document. Browser events could therefore fail with an `Unknown component id` server error.

### Fix

- `pl.run(app_factory=...)` now passes the initial application template into the ASGI runtime.
- The ASGI runtime aligns component IDs on each fresh factory-created component tree with the IDs used by the rendered session document.
- The original public `app_factory` callable is preserved.
- Session creation continues to use a fresh component tree and a separate `WebSocketServer` session.

### Public API Usage

Applications should use the existing public `pl.run(app_factory=...)` API:

```python
import pylage as pl

def create_app():
    # Create fresh state and a fresh component tree.
    ...
    return app

if __name__ == "__main__":
    pl.run(
        app_factory=create_app,
        serve=True,
        host="127.0.0.1",
        port=3000,
    )
```

The application factory must return a fresh `Component` tree for each session.

### Private API Boundary

Application code must not depend on private PyLage internals such as `_resolve_app` or `_align_component_ids`. Component ID alignment and session setup are runtime responsibilities handled internally by PyLage.

### Persistence Boundary

Session isolation does not provide durable application persistence. Data that must survive a browser reload, process restart, or deployment must be stored by the application in an appropriate persistence layer such as SQLite or PostgreSQL.

## Verification

- Foundation test suite: `327 passed`
- `git diff --check`: clean
- Dual-browser session isolation verified in the PyLage SaaS case study.
- Browser A state was not visible in Browser B.
- Browser B state was not visible in Browser A.
- Timers remained independent between browser sessions.
- Navigation remained free of `Unknown component id` errors.
