# PyLage UI Kit — Table

## Definition

`table` is a PyLage UI Kit component for displaying structured data as a semantic table.

It is a thin wrapper around the existing engine `Table`, adding UI Kit container styling while preserving the engine table behavior.

## Use

Use `table()` when application data needs to be displayed in a tabular layout.

The underlying engine handles data normalization and table rendering. The UI Kit wrapper provides the public API, semantic defaults, and style merging.

## Usage

### Record Dictionaries

```python
import pylage as pl

pl.table([
    {"Name": "Rachit", "Age": 24},
    {"Name": "Rahul", "Age": 25},
])
```

### Column Mapping

```python
import pylage as pl

pl.table({
    "Name": ["Rachit", "Rahul"],
    "Age": [24, 25],
})
```

### Rows with Explicit Headers

Explicit headers can be supplied when using positional row data:

```python
import pylage as pl

pl.table(
    [[1, "Rachit"], [2, "Rahul"]],
    headers=["ID", "Name"],
)
```

### DataFrame-like Data

DataFrame-like objects can be passed directly when they provide the behavior expected by the underlying engine `Table`.

```python
import pylage as pl

pl.table(dataframe)
```

The PyLage UI Kit does not require pandas itself. DataFrame support is provided through the underlying table implementation.

### Explicit Headers

The optional `headers` argument can be used to provide column names explicitly:

```python
import pylage as pl

pl.table(
    [[1, "Rachit"], [2, "Rahul"]],
    headers=["ID", "Name"],
)
```

## API

```python
table(data=None, *, headers=None, style=None, **props)
```

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `data` | `Any` | `None` | Table data passed to the underlying `Table`. |
| `headers` | `Any` | `None` | Optional explicit column headers passed to the underlying `Table`. |
| `style` | `Style \\| None` | `None` | Custom styles merged over the UI Kit table defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying `Table`. |

The wrapper does not define a separate data-normalization API. Supported data forms and rendering behavior are provided by the existing engine `Table`.

## Input Handling

The UI Kit passes `data` and `headers` directly to the engine `Table`.

The existing table implementation supports structured table data, including record dictionaries, column mappings, row data with explicit headers, and DataFrame-like objects.

When the supplied data format provides column names, headers can be inferred by the underlying implementation unless explicit `headers` are provided.

## Default Styling

The UI Kit wrapper applies the following default table container styling:

- `width: 100%`
- `border: 1px solid var(--color-border)`
- `border_radius: var(--radius-lg)`
- `overflow: hidden`

These defaults use existing PyLage design tokens for the border and radius.

## Styling Behavior

Custom styles are merged over the UI Kit defaults.

For example:

```python
import pylage as pl

pl.table(
    users,
    style=pl.style(width="80%"),
)
```

The supplied style overrides matching defaults while unrelated defaults remain available.

## Props and Compatibility

Additional keyword properties are forwarded to the underlying `Table` component.

For example, supported engine properties can be supplied without the UI Kit wrapper defining them as separate parameters.

The UI Kit wrapper is additive and does not replace the existing engine `Table` API.

## Reactive Data

`table()` delegates rendering and supported reactive behavior to the existing engine `Table` and PyLage runtime.

The UI Kit wrapper does not introduce a separate table state or data-binding system.

## HTML Safety

Table cell rendering and HTML escaping are handled by the existing PyLage table renderer rather than by the UI Kit wrapper.

Application data is therefore processed according to the engine table rendering contract.

## Scope

The current UI Kit `table()` component provides a public data-table wrapper and semantic table presentation.

It does not claim full feature parity with higher-level dataframe products such as built-in client-side sorting, filtering, pagination, column editing, or virtualization unless those capabilities are provided by the underlying engine.

## Architecture

```text
pl.table()
    ↓
UI Kit table wrapper
    ↓
PyLage ENGINE Table
    ↓
Existing renderer / reactive runtime
```

The UI Kit layer supplies the public wrapper and default styling. Data normalization and HTML table rendering remain owned by the existing engine.

## API Boundary

`table()` is the public UI Kit entry point.

It returns the existing engine `Table` component rather than introducing a second table renderer, data engine, or reactive runtime.

## Verified Working Example

The project provides two table demos:

- `demo/demo_table.py`
- `demo/demo_table_dataframe.py`

These provide working examples of the public table API and table-oriented data usage.

## Verification

Table behavior is covered by:

- `test/components/test_table.py`
- `test/components/test_ui_kit_table.py`
- `test/foundation/test_table_theme_foundation.py`
- `test/performance/test_large_table.py`

The verification sources cover the table component, UI Kit wrapper behavior, theme styling foundation, and large-table performance coverage.

## Verified Sources

- `pylage/UI/components/table.py`
- `demo/demo_table.py`
- `demo/demo_table_dataframe.py`
- `test/components/test_table.py`
- `test/components/test_ui_kit_table.py`
- `test/foundation/test_table_theme_foundation.py`
- `test/performance/test_large_table.py`
- `documents/table.md`

## Status

**Table documentation refined and verified.**
