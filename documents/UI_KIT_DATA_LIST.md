# UI Kit Data List

`pylage_ui.data_list()` formats structured key-value data, metadata specs, and resource properties into clean, accessible rows.

## Basic Usage

```python
import pylage as pl

pl.data_list({
    "Full Name": "Alice Henderson",
    "Department": "Product Design",
    "Location": "San Francisco, CA",
})
```

## Using Tuples or Lists

```python
import pylage as pl

pl.data_list([
    ("Host", "db-primary.internal"),
    ("Port", "5432"),
    ("Status", pl.badge("Online", variant="success")),
])
```

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `data` | `Mapping \| list` | — | Dictionary or list of tuples / items to display |
| `orientation` | `str` | `"horizontal"` | `"horizontal"` (split row) or `"vertical"` (stacked) |
| `divided` | `bool` | `True` | Whether to display subtle divider borders between entries |
| `style` | `Style` | `None` | Custom style overrides merged with default container style |
| `**props` | `Any` | — | Forwarded to root component |

## Vertical Layout

```python
import pylage as pl

pl.data_list({
    "API Key": "pk_live_51M0...92b",
    "Webhook Secret": "whsec_08f...c89",
}, orientation="vertical")
```
