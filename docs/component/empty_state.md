# PyLage UI Kit — Empty State

## Definition

`empty_state()` is a semantic, high-level UI Kit component for presenting an empty or zero-data view. It composes an optional icon, title, description, and action inside a styled PyLage `Column`.

## Use

Use `empty_state()` when a page, dashboard, table, list, search result, or similar view has no content to display.

Common uses include:

- Empty project or workspace lists
- No search results
- Empty notification or task views
- Empty tables and data views
- Providing an action that helps the user recover from an empty state

## Usage

### Basic empty state

```python
import pylage as pl

pl.empty_state(
    title="No projects found",
    description="You have not created any projects yet.",
)
```

### With icon

String icons are rendered inside the component using the UI Kit icon-container styling.

```python
import pylage as pl

pl.empty_state(
    title="No notifications",
    description="You are all caught up.",
    icon="🔔",
)
```

### With an action

An existing PyLage component can be supplied as the `action`.

```python
import pylage as pl

pl.empty_state(
    title="No projects found",
    description="Get started by creating your first project.",
    icon="📁",
    action=pl.button("New Project", variant="primary"),
)
```

### In a layout

`empty_state()` can be composed with normal PyLage layout components.

```python
import pylage as pl

pl.grid(
    pl.empty_state(
        title="No notifications",
        description="There are no unread notifications.",
        icon="🔔",
    ),
    pl.empty_state(
        title="No projects found",
        description="Create your first project to get started.",
        icon="📁",
        action=pl.button("New Project", variant="primary"),
    ),
)
```

## API

```python
empty_state(
    title="No data found",
    description="There are no items or records to display at this time.",
    *, 
    icon=None,
    action=None,
    style=None,
    **props,
)
```

### Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `title` | `Any` | `"No data found"` | Content used for the empty-state heading. |
| `description` | `Any` | `"There are no items or records to display at this time."` | Supporting description shown below the title. |
| `icon` | `Any` | `None` | Optional icon content. Strings receive the built-in icon-container styling; other values are inserted as components/content. |
| `action` | `Any` | `None` | Optional action component, such as a PyLage button. |
| `style` | `Style` | `None` | Optional style merged with the default container style. |
| `**props` | `Any` | — | Additional properties forwarded to the root `Column`. |

## Content Behavior

The component builds its contents in this order:

1. `icon`, when supplied
2. `title`, when not `None`
3. `description`, when not `None`
4. `action`, when supplied

Both `title` and `description` can be omitted by passing `None`. The `icon` and `action` are also optional.

## Default Styling

The root container uses:

- `display: flex`
- `flex-direction: column`
- `align-items: center`
- `justify-content: center`
- `text-align: center`
- `padding: var(--spacing-2xl)`
- `background-color: var(--color-background)`
- `border: 1px dashed var(--color-border-muted)`
- `border-radius: var(--radius-xl)`
- `gap: var(--spacing-sm)`

The title, description, and string icon also receive dedicated UI Kit styles.

## Styling Behavior

The optional `style` is merged with the default container style:

```python
final_style = _DEFAULT_CONTAINER_STYLE.merge(style)
```

Explicit style values therefore override matching container defaults while unspecified defaults remain active.

For example:

```python
import pylage as pl

pl.empty_state(
    title="No records",
    style=pl.style(
        padding="3rem",
        background_color="#f8fafc",
    ),
)
```

## Composition

`empty_state()` returns a PyLage `Column` containing the generated content. Existing PyLage components can therefore be used for actions and other supported content values.

## API Boundary

The UI Kit component owns the empty-state structure and default styling. Additional `**props` are forwarded to the root `Column`, allowing engine-supported properties such as `class_name` and `id` to be used.

## Verified Working Example

The project demo `demo/demo_empty_state.py` renders three empty-state variants in a responsive grid: a notification state with an icon, a project state with an icon and primary action, and a search state with an icon and outline action.

## Verification

Verified coverage includes:

- Returns a PyLage `Column`
- Default title and description
- Custom title and description
- String icon rendering
- Action component rendering
- Custom style overrides
- Engine property forwarding through `class_name` and `id`

## Verified Sources

- `pylage/UI/components/empty_state.py`
- `demo/demo_empty_state.py`
- `test/components/test_ui_kit_empty_state.py`
- `documents/empty_state.md` (reference/archive)

## Status

Empty State documentation is refined against the current implementation, demo, and verified tests.
