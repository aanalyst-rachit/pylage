# PyLage UI Kit — Table

## Overview

pl.table() provides a semantic data-table API while reusing the existing PyLage Table component and renderer.

It is designed so application data can be passed directly to the UI Kit without requiring users to manually construct table rows.

Example:

    import pylage as pl

    pl.table([
        {"Name": "Rachit", "Age": 24},
        {"Name": "Rahul", "Age": 25},
    ])

## DataFrame Usage

DataFrame-like objects can be passed directly as the first argument, including pandas DataFrames when pandas is installed.

Example:

    import pandas as pd
    import pylage as pl

    users = pd.DataFrame({
        "Name": ["Rachit", "Rahul"],
        "Age": [24, 25],
    })

    table = pl.table(users)

Pandas is not a required PyLage dependency. The engine uses DataFrame-like behavior rather than importing pandas itself.

Polars DataFrame/LazyFrame-like objects are also supported when the corresponding library is available.

## Supported Input Forms

pl.table() delegates data normalization to the existing PyLage Table component.

Supported forms include:

### Record dictionaries

    pl.table([
        {"Name": "Rachit", "Age": 24},
        {"Name": "Rahul", "Age": 25},
    ])

### Column mapping

    pl.table({
        "Name": ["Rachit", "Rahul"],
        "Age": [24, 25],
    })

### Rows with explicit headers

    pl.table(
        [[1, "Rachit"], [2, "Rahul"]],
        headers=["ID", "Name"],
    )

### DataFrame-like objects

Objects exposing the expected DataFrame-style columns and conversion/row APIs can be passed directly.

    pl.table(dataframe)

## API

    pl.table(data=None, *, headers=None, style=None, **props)

### Parameters

- data — table data. Supports records, column mappings, rows, and DataFrame-like objects.
- headers — optional explicit column headers. When omitted, headers are inferred where the data format provides them.
- style — optional pylage.Style merged over semantic UI Kit defaults.
- props — forwarded to the underlying PyLage Table component.

## Headers

Explicit headers are useful when passing positional row data:

    pl.table(
        [[1, "Rachit"], [2, "Rahul"]],
        headers=["ID", "Name"],
    )

For record dictionaries and DataFrame-like objects, headers are inferred from the available column names unless explicitly overridden.

## Reactive Data

The UI Kit delegates rendering to the existing PyLage component and state system. Data and headers can therefore participate in existing reactive workflows where supported by the underlying renderer.

The UI Kit does not introduce a separate table state or data-binding system.

## Styling

pl.table() provides semantic defaults using existing PyLage design tokens:

- Full-width table layout.
- Standard border token.
- Large radius token.
- Hidden overflow for the table container.

Custom Style values are merged over these defaults:


    import pylage as pl

    pl.table(
        users,
        style=pl.style(width="80%"),
    )

## HTML Safety

Table cell values are escaped by the existing PyLage renderer before being inserted into HTML. Application data is not treated as raw HTML by default.

## Props and Compatibility

Additional properties are forwarded to the existing PyLage Table component:

    pl.table(
        users,
        title="Users",
        class_name="users-table",
    )

Existing engine-level Table usage remains supported. The UI Kit is additive and does not replace the underlying pylage.Table API.

## Architecture

pl.table() is a WRAP implementation. It does not introduce a second table renderer, state engine, data-normalization engine, CSS engine, or layout engine.

Architecture:

User API → pylage_ui.table → pylage.Table → existing renderer/reactive runtime

Data normalization and HTML rendering remain owned by the PyLage engine.

## Scope

The current Table component provides data ingestion and semantic HTML rendering.

It does not claim full Streamlit st.dataframe() feature parity such as built-in client-side sorting, filtering, pagination, column editing, or virtualization.

Those capabilities can be added later without changing the basic pl.table(data) API.

## Manual Demo

See demo/demo_table_dataframe.py for the browser/manual smoke example.
