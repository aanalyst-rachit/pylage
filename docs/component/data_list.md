# PyLage UI Kit — Data List

## Definition

`data_list()` creates a structured key-value list for displaying resource details, metadata, specifications, and similar information. It reuses the existing PyLage Engine `Column`, `Row`, and `Text` components.

## Use

Use `data_list()` when related labels and values should be presented as a consistent information panel. It supports:

- Dictionary-based key-value data
- Lists of `(label, value)` tuples
- Lists of mappings with `label` and `value` fields
- Existing PyLage components as labels or values
- Horizontal or vertical layouts
- Optional divider borders between entries

## Usage

### Dictionary data

```python
import pylage as pl

pl.data_list({
    "Full Name": "Alice Henderson",
    "Department": "Product Design",
    "Location": "San Francisco, CA",
})
```

### Tuple data

```python
import pylage as pl

pl.data_list([
    ("Host", "db-primary.internal"),
    ("Port", "5432"),
    ("Status", pl.badge("Online", variant="success")),
])
```

### List of mappings

Each mapping may provide `label` and `value` keys:

```python
import pylage as pl

pl.data_list([
    {"label": "CPU", "value": "4 Cores"},
    {"label": "Memory", "value": "16 GB"},
])
```

### Vertical layout

```python
import pylage as pl

pl.data_list({
    "Primary Region": "ap-south-1",
    "Backup Node": "ap-south-2",
    "Storage Used": "42.8 GB / 100 GB",
}, orientation="vertical")
```

### Component values

Existing components are preserved instead of being wrapped in `Text`, so values such as badges can be used directly.

```python
import pylage as pl

pl.data_list({
    "Status": pl.badge("Healthy", variant="success"),
})
```

## API

```python
data_list(
    data,
    orientation="horizontal",
    divided=True,
    style=None,
    **props,
)
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Mapping[str, Any]` or list | — | Source data converted into label/value entries. |
| `orientation` | `str` | `"horizontal"` | Controls whether entries use horizontal rows or vertical stacks. |
| `divided` | `bool` | `True` | Adds a bottom divider to every entry except the last one. |
| `style` | `Style` or `None` | `None` | Custom root-container styles merged after the defaults. |
| `**props` | `Any` | — | Additional properties forwarded to the root Engine `Column`. |

## Data Resolution

`data` is normalized into a list of `(label, value)` pairs.

- A `Mapping` is converted using its `.items()`.
- A list or tuple containing mappings reads `label` and `value` from each mapping.
- A list or tuple containing another list or tuple uses its first two elements as label and value when at least two elements exist.
- Other list entries become values with an empty label.

Labels and values that are already components are preserved. Other values are wrapped in Engine `Text` components.

## Composition Behavior

The root component is an Engine `Column`. Each normalized item becomes either an Engine `Row` or Engine `Column` depending on `orientation`.

```text
data_list
├── row / column entry
│   ├── label
│   └── value
├── row / column entry
│   ├── label
│   └── value
└── ...
```

For horizontal orientation, each entry uses a horizontal Engine `Row` with space-between alignment.

For vertical orientation, each entry uses an Engine `Column` with a small gap between the label and value.

## Default Styling

The root container uses:

- `display="flex"`
- `flex_direction="column"`
- `width="100%"`
- `background_color="var(--color-background)"`
- `border="1px solid var(--color-border)"`
- `border_radius="var(--radius-xl)"`
- `padding="var(--spacing-md)"`
- `gap="var(--spacing-sm)"`

Labels use muted text styling, while values use the normal text color.

Horizontal entries use:

- `display="flex"`
- `flex_direction="row"`
- `justify_content="space-between"`
- `align_items="center"`
- `padding="var(--spacing-xs) 0"`
- `width="100%"`

Vertical entries use a column layout with `0.25rem` internal gap and the same horizontal padding convention.

## Divider Behavior

When `divided=True`, every entry except the last receives a bottom border using `var(--color-border-muted)` and additional bottom spacing.

The default is `divided=True`. Set `divided=False` when entries should not have separators.

## Styling Behavior

The final root style is built as:

```python
final_style = _DEFAULT_CONTAINER_STYLE.merge(style)
```

Therefore, values supplied through `style` override the default container styling.

For example:

```python
import pylage as pl

pl.data_list(
    {"Environment": "Staging"},
    style=pl.style(
        padding="2rem",
        background_color="#f8fafc",
    ),
)
```

## API Boundary

`data_list()` is a composition helper. It does not implement its own renderer or DOM system.

```text
data_list()
        ↓
Engine Column / Row / Text
        ↓
PyLage renderer and runtime
        ↓
HTML / browser
```

Engine properties supplied through `**props`, such as `class_name` and `id`, are forwarded to the root `Column`.

## Verified Working Example

The project demo uses dictionary data, tuple data, component values, and vertical orientation:

```python
import pylage as pl
import pylage as pl

pl.data_list({
    "Account": "Enterprise Cloud",
    "Subscription": pl.badge("Active", variant="success"),
    "Billing Cycle": "Monthly (Auto-renew)",
    "Renewal Date": "October 1, 2026",
})

pl.data_list([
    ("Host", "api.pylage.dev"),
    ("Cluster", "us-east-4"),
    ("Uptime", "99.98%"),
    ("Health", pl.badge("Healthy", variant="success")),
])

pl.data_list({
    "Primary Region": "ap-south-1",
    "Backup Node": "ap-south-2",
    "Storage Used": "42.8 GB / 100 GB",
}, orientation="vertical")
```

## Verification

The component is covered by `test/components/test_ui_kit_data_list.py`.

Verified behavior includes:

- Returns an Engine `Column`.
- Renders dictionary data.
- Renders tuple-based data.
- Renders lists of mappings.
- Supports vertical orientation.
- Preserves existing components as values.
- Applies custom root styles.
- Forwards Engine properties such as `class_name` and `id`.

## Verified Sources

- Component source: `pylage/UI/components/data_list.py`
- Demo: `demo/demo_data_list.py`
- Tests: `test/components/test_ui_kit_data_list.py`
- Reference documentation: `documents/data_list.md`

## Status

**FINAL / VERIFIED**
