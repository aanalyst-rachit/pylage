# Patterns API

Canonical URI: `/api/patterns/`

PyLage patterns are higher-level reusable UI sections built from public components.

## Available patterns

- `pl.hero` — Hero section for prominent page introductions.
- `pl.feature_section` — Feature-focused content section.
- `pl.content_section` — Structured content section.
- `pl.contact_section` — Contact-oriented section.
- `pl.faq` — Frequently asked questions section.
- `pl.cta` — Call-to-action section.
- `pl.newsletter_section` — Newsletter signup section.
- `pl.pricing_section` — Pricing plans section.
- `pl.testimonial` — Testimonial section.
- `pl.search_bar` — Search interface pattern.
- `pl.stats_section` — Statistics/metrics presentation section.

## Example

```python
import pylage as pl

page = pl.hero(
    title="Build with PyLage",
    subtitle="Declarative Python UI",
)
```

## Implementation references

- `pylage/UI/patterns/`
