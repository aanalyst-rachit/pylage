# Recipes API

Canonical URI: `/api/recipes/`

PyLage recipes provide ready-made application-level compositions for common page types.

## `pl.admin_panel`

Provides an admin-oriented application composition.

## `pl.authentication`

Provides authentication-oriented application composition.

## `pl.dashboard_page`

Provides a ready-made dashboard page composition.

## `pl.landing_page`

Provides a landing-page composition.

## `pl.profile_page`

Provides a profile-page composition.

## Example

```python
import pylage as pl

page = pl.landing_page(
    title="Welcome",
    subtitle="Build your application with PyLage.",
)
```

## Implementation references

- `pylage/UI/recipes/`
