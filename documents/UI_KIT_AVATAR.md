# UI Kit Avatar

## Overview

`pl.avatar()` provides a semantic UI Kit avatar by composing the existing PyLage `Avatar` primitive.

## API

```python
import pylage as pl

pl.avatar("RK")
pl.avatar("Rachit Kumar", size="lg")
pl.avatar(pl.Image(src="https://example.com/avatar.png", alt="User"))
```

## Sizes

| Size | Width | Height |
| --- | --- | --- |
| `sm` | 32px | 32px |
| `md` | 40px | 40px |
| `lg` | 48px | 48px |

## Content

Primitive content is normalized into the existing PyLage `Text` component. Existing PyLage components such as `Image` can be composed directly.

## Customization

Custom `Style` values are merged after the UI Kit defaults, so explicit user styles override defaults.

## Architecture

Avatar is a UI Kit composition layer. It does not introduce a new renderer, styling engine, or avatar-specific rendering system.
