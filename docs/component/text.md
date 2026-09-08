# PyLage UI Kit — Text

## Definition

`text` is a PyLage UI component exposed through the UI Kit.

The following documentation is generated from the current component source, running demo, tests, and existing documentation.

## Use

## Usage

The project demo provides the primary running usage example: `demo/demo_text.py`.

Detected calls in the demo:

- `column()`
- `get_app()`
- `rgba()`
- `style()`
- `text()`

## Working Example

```python
import pylage as pl

pl.text("Hello PyLage")
```

```python
pl.text("Secondary information", muted=True)
```

```python
pl.text("Email address", label=True)
```

```python
pl.text("Last updated today", caption=True)
```

```python
import pylage as pl

pl.text(
    "Custom text",
    muted=True,
    style=pl.style(color="#123456"),
)
```

## API

```python
text(value, muted=False, label=False, caption=False, style=None, **props)
```

## Additional Documentation

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `value` | `Any` | — | Text content |
| `muted` | `bool` | `False` | Applies muted text styling |
| `label` | `bool` | `False` | Applies label styling |
| `caption` | `bool` | `False` | Applies caption styling |
| `style` | `Style \| None` | `None` | Custom styles merged last |
| `**props` | `Any` | — | Forwarded to the underlying PyLage Text |

### Style Precedence

Semantic UI Kit styles are applied first. An explicit `style` is merged last, so custom values take precedence.

```python
import pylage as pl

pl.text(
    "Custom text",
    muted=True,
    style=pl.style(color="#123456"),
)
```

## Verified Sources

- Component source: `pylage/UI/components/text.py`
- Demo: `demo/demo_text.py`
- Test: `test/components/test_text.py`
- Test: `test/components/test_textarea.py`
- Test: `test/components/test_ui_kit_text.py`
- Test: `test/foundation/test_registry_generic_text_contract.py`
- Existing documentation: `documents/text.md`

## Verification Status

- Component source inspected.
- Demo found: yes.
- Tests found: 4.
- Public API detected: yes.
- Existing documentation found: yes.

> This file is generated evidence documentation. Final prose should be reviewed against the implementation before publication.

## Other Details

`text()` creates semantic text using the existing PyLage Text component.
## Basic Usage
## Semantic Options

### Muted


### Label
### Caption

## Parameters
## Style Precedence
## Architecture
```text
pl.text()
    ↓
UI Kit text wrapper
    ↓
PyLage Text
    ↓
Existing renderer
```
