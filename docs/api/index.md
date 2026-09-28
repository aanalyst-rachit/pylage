# PyLage Public API Reference

This section is the canonical reference for the stable names exported by `import pylage as pl`.

The API reference provides a stable documentation URI for every public export. Detailed component guides remain the authoritative behavioral documentation where they already exist.

## Reference sections

- [Application](application.md) — `pl.app()`, `pl.run()`, version information, and runtime selection.
- [State and Reactivity](state.md) — state, derived values, reactive collections, and conditional/reactive rendering.
- [Routing](routing.md) — routes, routers, and routing runtime.
- [Styling and Themes](styling.md) — styles, colors, themes, and theme helpers.
- [Layout](layout.md) — layout primitives, factories, and navigation layouts.
- [Patterns](patterns.md) — reusable UI patterns and sections.
- [Recipes](recipes.md) — higher-level application compositions.
- [Components and Primitives](components.md) — public UI components and lower-level primitives.

## Public API rule

The names exported by `pylage.__all__` are the stable root-level API surface. Internal modules, implementation helpers, and classes that are not exported from `pylage` are not automatically public API.
