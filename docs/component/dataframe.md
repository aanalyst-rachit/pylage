# PyLage UI Kit — DataFrame

## Definition

`dataframe()` creates a high-level spreadsheet-like data view using the existing PyLage Engine `DataFrame` component. The UI Kit wrapper adds default presentation styling and forwards the data and DataFrame options to the existing engine implementation.

## Use

Use `dataframe()` for dense tabular data where a DataFrame-style presentation is appropriate. It supports:

- DataFrame-like objects
- Lists of mappings or row data
- Explicit column headers
- Optional cell borders
- Custom root styling
- Existing PyLage rendering infrastructure

## Usage

### Row data

```python
import pylage as pl

pl.dataframe([
    {"Name": "Rachit", "Score": 95},
    {"Name": "Rahul", "Score": 91},
])
```

### Explicit headers

```python
import pylage as pl

pl.dataframe(
    [[
        1, "Rachit"
    ], [2, "Rahul"]],
    headers=["ID", "Name"],
)
```

### DataFrame-like objects

Objects exposing the expected DataFrame-style interface can be passed directly. Pandas is not required by the UI Kit wrapper.

```python
import pylage as pl

pl.dataframe(my_dataframe)
```

When pandas is installed, a pandas `DataFrame` can also be passed directly.

### Disable cell borders

Cell borders are enabled by default and can be disabled independently from the outer DataFrame border.

```python
import pylage as pl

pl.dataframe(
    rows,
    cell_border=False,
)
```

### Custom styling

```python
import pylage as pl

pl.dataframe(
    rows,
    style=pl.style(width="80%"),
)
```

## API

```python
dataframe(
    data,
    headers=None,
    style=None,
    cell_border=True,
    **props,
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Any` | — | Data supplied to the underlying Engine `DataFrame`. |
| `headers` | `Any` | `None` | Optional explicit column headers. |
| `style` | `Style` or `None` | `None` | Custom root styles merged after the UI Kit defaults. |
| `cell_border` | `bool` | `True` | Controls whether individual cell borders are rendered. |
| `**props` | `Any` | — | Additional properties forwarded to the underlying Engine `DataFrame`. |

## Data Support

The wrapper accepts `data` as `Any` and passes it directly to the existing Engine `DataFrame`.

Verified inputs include:

- Lists of mappings.
- Lists of row lists with explicit `headers`.
- DataFrame-like objects providing `columns` and `to_dict(orient="records")`.
- Pandas DataFrames when pandas is installed.

The wrapper itself does not import pandas, so pandas is not a required dependency for the UI Kit API.

## Styling Behavior

The UI Kit defines these default root styles:

- `width="100%"`
- `border="1px solid var(--color-border)"`
- `border_radius="var(--radius-lg)"`
- `overflow="hidden"`

The final root style is created with:

```python
final_style = _DEFAULT_STYLE.merge(style)
```

Therefore, values supplied through `style` override the corresponding UI Kit defaults.

## Cell Border Behavior

`cell_border=True` is the default.

When enabled, the rendered DataFrame includes individual cell border rules.

When `cell_border=False`, the Engine adds the no-cell-border presentation and removes individual cell right and bottom borders. The outer DataFrame border remains present.

This means disabling cell borders changes the grid presentation; it does not remove the DataFrame container itself.

## API Boundary

`dataframe()` is a wrapper around the existing Engine `DataFrame`. It does not introduce a separate table renderer or data engine.

```text
dataframe()
        ↓
Engine DataFrame
        ↓
PyLage renderer and runtime
        ↓
HTML / browser
```

The wrapper supplies default styling, forwards `headers` and `cell_border`, and passes additional properties through to the Engine component.

## DataFrame vs Table

`dataframe()` is intended for spreadsheet-like data presentation and accepts DataFrame-style inputs.

`table()` is a separate UI Kit API for structured table composition. The two components should not be treated as interchangeable APIs.

## Verified Working Example

The project demo loads the real `test.csv` dataset and demonstrates both bordered and borderless DataFrame views:

```python
import pylage as pl

pl.dataframe(
    rows,
    title="test.csv — bordered grid",
    class_name="test-csv-grid",
)

pl.dataframe(
    rows[:8],
    title="test.csv — no cell borders",
    cell_border=False,
    class_name="test-csv-grid-no-border",
)
```

## Verification

The component is covered by `test/components/test_ui_kit_dataframe.py`.

Verified behavior includes:

- Returns and renders the existing Engine DataFrame.
- Accepts DataFrame-like objects.
- Accepts explicit headers with row data.
- Works without pandas.
- Accepts a real pandas DataFrame when pandas is available.
- Merges custom styles with the UI Kit defaults.
- Enables cell borders by default.
- Supports disabling individual cell borders.
- Preserves the outer DataFrame border when cell borders are disabled.

## Verified Sources

- Component source: `pylage/UI/components/dataframe.py`
- Demo: `demo/demo_dataframe.py`
- Tests: `test/components/test_ui_kit_dataframe.py`
- Reference documentation: `documents/dataframe.md`

## Status

**FINAL / VERIFIED**
