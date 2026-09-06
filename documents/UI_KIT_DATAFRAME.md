# UI Kit DataFrame

## Overview

`ps.dataframe()` is the high-level UI Kit API for spreadsheet-like tabular data.

It reuses the existing PyLage DataFrame component, renderer, styling system, and reactive runtime.

The UI Kit does not introduce a separate rendering or data engine.

## Architecture

The implementation follows the UI Kit design contract:

```text
User Application
      ↓
pylage_ui.dataframe()
      ↓
pylage.DataFrame
      ↓
Existing DataFrame Renderer
      ↓
Existing PyLage Runtime

Classification: WRAP

The UI Kit adds the semantic high-level API and presentation defaults while reusing existing PyLage infrastructure.
Presentation

The DataFrame provides a spreadsheet-like presentation with:

    column headers

    row-number gutter

    scrollable data viewport

    sticky header

    sticky row-number gutter

    compact cells

    numeric alignment

    cell clipping

    hover feedback

    configurable cell borders

DataFrame-Like Objects

Pandas is not a required PyLage dependency. The implementation works with DataFrame-like objects without importing pandas itself.

When pandas is installed, a pandas DataFrame can also be passed directly.
DataFrame vs Table

ps.table() is the semantic structured-table API.

ps.dataframe() is intended for a denser, spreadsheet-like presentation with row numbers, sticky navigation, compact cells, numeric alignment, and DataFrame-like inputs.

Both reuse the existing PyLage rendering infrastructure.
DataFrame vs Data List

Disabling cell borders does not turn a DataFrame into a Data List. It only changes the visual presentation.

A future ps.list() can provide record-oriented layouts such as title/subtitle rows, avatars, actions, and mobile-friendly items.

Generic ps.row(), ps.card(), and related composition primitives can already be used for custom lists.
Current Scope

The current implementation provides:

    DataFrame-like input

    optional headers

    spreadsheet-like rendering

    scrolling

    sticky headers

    sticky row-number gutter

    compact cells

    numeric alignment

    clipping

    hover feedback

    cell borders

    borderless cell mode

    existing PyLage styling

    existing PyLage reactive/runtime behavior

The implementation does not currently claim:

    sorting

    filtering

    pagination

    column editing

    column resizing

    virtualization

Manual Demo

Manual demonstration:

demo/demo_dataframe.py

The demo uses the project dataset and demonstrates normal rendering, cell borders, borderless cells, and scrolling.
Tests

Focused tests:

test/test_ui_kit_dataframe.py

Coverage includes DataFrame-like input, headers, style merging, optional pandas support, cell borders, and preservation of the outer border.