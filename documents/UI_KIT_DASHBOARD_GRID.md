# UI Kit Dashboard Grid

`pylage_ui.dashboard_grid()` arranges analytics cards, widgets, and charts into responsive layouts using standardized grid presets.

## Basic Usage

```python
import pylage as pl

pl.dashboard_grid(
    pl.card(heading="Sales", body="1,200 units"),
    pl.card(heading="Traffic", body="45K visitors"),
    layout="2-col",
)
```

## Layout Presets

Supported presets via `layout=`:
- `"auto"`: Responsive auto-fit columns (`minmax(340px, 1fr)`)
- `"2-col"`: 2 equal-width columns
- `"3-col"`: 3 equal-width columns
- `"main-side"`: 2fr main column, 1fr side column
- `"side-main"`: 1fr side column, 2fr main column

## Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `*widgets` | `Any` | — | Positional widget cards or components |
| `layout` | `str` | `"auto"` | Grid preset name |
| `columns` | `int \| str` | `None` | Custom column definition overriding preset |
| `gap` | `str` | `None` | Custom gap spacing overriding default `SPACING["xl"]` |
| `style` | `Style` | `None` | Custom style overrides merged with default grid style |
| `**props` | `Any` | — | Forwarded to root `Grid` |
