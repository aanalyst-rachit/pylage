# State & Reactivity API

Canonical URI: `/api/state/`

State APIs provide reactive values, derived state, conditional rendering, and reactive collections.

## `pl.state`

Creates a reactive state value.

```python
import pylage as pl

count = pl.state(0)
```

Read the current value with `count.value` and update it by assigning a new value.

## `pl.derived`

Creates a value derived from other reactive state.

```python
total = pl.derived(lambda: count.value * 2)
```

The derived value updates when its dependencies change.

## `pl.reactive_list`

Creates a reactive list suitable for UI collections.

```python
items = pl.reactive_list(["One", "Two"])
```

Use it when list mutations need to participate in PyLage reactivity.

## `pl.for_each`

Renders UI from a reactive or dynamic collection.

```python
pl.for_each(items, lambda item: pl.text(item))
```

## `pl.cond`

Conditionally renders one of two branches.

```python
pl.cond(
    count.value > 0,
    pl.text("Active"),
    pl.text("Empty"),
)
```

## Implementation references

- `pylage/ENGINE/state/`
- `pylage/ENGINE/core/reactive_list.py`
