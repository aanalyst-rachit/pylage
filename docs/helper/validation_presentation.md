# UI Kit Validation Presentation

## Overview

Phase 08 validation presentation is provided through the existing `form_field()` composition component and the existing `error_state()` component.

No separate validation renderer or validation UI implementation is required.

## Field-Level Validation

Use `form_field(error=...)` to present validation feedback next to an existing form control:

```python
import pylage as pl

pl.form_field(
    pl.input(value="invalid@example"),
    label="Email",
    error="Please enter a valid email address.",
)
```

`form_field()` is responsible for presentation only. Validation logic remains the responsibility of the application or validation layer.

## Page-Level Error Feedback

Use the existing `error_state()` component for larger operation, page, or system-level failures:

```python
import pylage as pl

pl.error_state(
    title="Failed to load dashboard",
    description="The remote service is currently unavailable.",
    action=pl.button("Retry", variant="danger"),
)
```

## Architecture

```text
Application validation logic
        │
        ├── field validation → form_field(error=...)
        │
        └── operation/page failure → error_state(...)
```

## Verification

- FormField automated tests cover error presentation.
- FormField browser verification covers rendered error content.
- ErrorState automated tests cover default, custom, action, styling, and forwarded properties.
- Existing manuals provide manual verification coverage.

## Status

Validation presentation is covered by existing UI Kit composition components and is complete for Phase 08.
