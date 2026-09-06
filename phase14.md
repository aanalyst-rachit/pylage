# PHASE 14 — CURRENT POSITION

**Current Step:** 14.1 — Public API Contract Lock
**Working File:** phase14.md — Phase 14 complete hone tak isi file ko working tracker maana jayega.
**Next Action:** Existing root API, Style, Theme, and Engine integration ka exact audit; implementation se pehle reuse/wrap/compose/build classification.
**Public API Rule:** User-facing API = `import pylage as pl` → `pl.*`.
**Internal Rule:** `pylage.UI.*` / `pylage.ENGINE.*` ko user-facing examples/docs/tests mein expose nahi karna; legitimate internals ko unnecessarily migrate nahi karna.
**Completion:** Phase 14 ke end par full regression + tracker update + Git checkpoint; uske baad `phase14.md` remove karna.

progress:-

14.1 [x]
14.2 [x]
14.3 [x]
14.4 [x]
14.5 [x]
14.6 [x]
14.7 [x]
14.8 [x]
14.9 [x]
14.10 [x]
14.11 [x]
14.12 [x]
14.13 [x]
14.14 [x]
14.15 [x]
14.16 [x]
14.17 [x]



## PHASE 14 — Customization Roadmap

### 🎯 Phase 14 Final Goal

User ko ideally sirf:

```python
import pylage as pl
```

karna ho.

Aur customization ka complete public surface:

```python
pl.card(...)
pl.button(...)

pl.style.black
pl.style.elevated_card

pl.theme.light
pl.theme.dark

pl.set_theme("dark")

pl.style(...)
```

Internal implementation:

```python
pylage.UI.*
pylage.ENGINE.*
```

**user-facing examples/docs/tests mein expose nahi honge.**

---

# 14.1 — Public API Contract Lock

Sabse pehle exact public API decide/freeze:

```text
pl.*
├── components
├── layouts
├── patterns
├── recipes
├── style
├── theme
├── set_theme()
├── customization helpers
└── tokens / colors (only if justified)
```

### Deliverables

* Root `pylage/__init__.py` audit
* `__all__` normalization
* naming consistency
* public vs internal boundary
* API contract tests

**Status:** audit partially done → implementation required.

---

# 14.2 — Style Public API

Current:

```python
from pylage import style

style.black
style.white
style.elevated_card
style.topheader
```

Isko proper `pl.*` contract banana hai.

Target:

```python
import pylage as pl

pl.style.black
pl.style.white
pl.style.elevated_card
```

Aur advanced customization ke liye:

```python
pl.style(...)
```

agar existing architecture allow karta hai.

### Is task mein:

* existing `Style` reuse
* duplicate style class nahi
* style presets migrate
* style constructor/public factory decide
* style validation
* style composition/merge
* style custom CSS properties
* style documentation/tests

---

# 14.3 — Style Usage Migration

**Ye important hai jo tumne bola.**

Sirf API expose karke nahi chhodenge.

Pure project mein audit:

```text
pylage/
test/
examples/
docs/
```

Aur identify:

```python
pylage.ENGINE.styling.Style
pylage.UI.style
from ...style import ...
```

etc.

### Rule

Internal implementation files ko unnecessarily public API par force nahi karenge.

Lekin:

* examples
* tests representing user usage
* documentation
* public recipes
* public component contracts

mein **canonical usage `import pylage as pl`** hoga.

Target:

```python
import pylage as pl

pl.card(..., style=pl.style.elevated_card)
```

instead of teaching users:

```python
from pylage.UI.style import elevated_card
```

---

# 14.4 — Variant System

Current button mein already:

```python
variant=
```

hai.

Isko Phase 14 mein **formal customization contract** banana hai.

Audit:

```text
button
badge
alert
dialog
...
```

### Goal

Where variants genuinely make semantic sense:

```python
pl.button(..., variant="primary")
pl.button(..., variant="danger")
```

But:

**har component mein artificial variants nahi add karne.**

Existing implementation reuse/standardize.

---

# 14.5 — Size System

Current button:

```python
size="sm"
size="md"
size="lg"
```

already has this.

Phase 14 mein:

* size semantics audit
* valid values
* component consistency
* default preservation
* invalid-value errors
* tests

Target:

```python
pl.button("Save", size="lg")
```

Aur existing components jahan size already meaningful hai, unko standardize karna.

---

# 14.6 — Theme Public API

Current infrastructure:

```python
LIGHT_THEME
DARK_THEME
get_theme()
available_themes()
```

already exists.

Isko public API mein clean karna:

```python
import pylage as pl

pl.theme.light
pl.theme.dark
```

plus:

```python
pl.set_theme("dark")
```

### Important

Theme ka **actual global application mechanism** audit karna hai.

Sirf:

```python
pl.theme.dark
```

return karna enough nahi hai.

---

# 14.7 — Global Theme System

Ye Phase 14 ka major task hai.

Target:

```python
import pylage as pl

pl.set_theme("dark")

pl.card(...)
pl.button(...)
```

Theme automatically rendering pipeline mein apply ho.

### Requirements

* global current theme
* default theme
* named theme lookup
* renderer integration
* CSS variable generation
* reset/change behavior
* invalid theme handling
* test isolation

Existing renderer/theme machinery ko reuse karna hai.

---

# 14.8 — Custom Theme / Custom Tokens

Preset:

```python
pl.set_theme("dark")
```

Advanced:

```python
custom_theme = ...
pl.set_theme(custom_theme)
```

Exact API audit ke baad decide hogi.

Theme should support semantic tokens such as:

```text
background
surface
surface_alt
text
text_muted
border
primary
secondary
success
warning
danger
info
```

### Goal

Components hard-coded colors par depend na karein.

They consume semantic theme variables.

---

# 14.9 — Semantic Colors Public Surface

Phase 14 mein decide karna:

```python
pl.colors.primary
pl.colors.success
pl.colors.danger
```

ya equivalent public mechanism.

**But only if existing architecture supports it cleanly.**

Important principle:

> CSS variables + semantic theme tokens remain the source of truth.

Duplicate color registry nahi banega.

---

# 14.10 — Component-Level Overrides

Existing:

```python
style=
```

support ko standardize karna.

Target:

```python
pl.card(
    "Hello",
    style=pl.style.elevated_card,
)
```

and:

```python
pl.button(
    "Save",
    style=...
)
```

### Audit every public component

Check:

* default style
* variant style
* size style
* user style
* merge precedence

Expected precedence:

```text
component defaults
    ↓
variant
    ↓
size
    ↓
semantic/custom props
    ↓
user style override
```

Exact precedence existing behavior ke according preserve/normalize karenge.

---

# 14.11 — Global Overrides

Phase 14 tracker ka:

> Global overrides

Iska proper mechanism design karna hai.

Conceptually:

```python
pl.configure(...)
```

ya equivalent — **exact name audit ke baad decide hoga.**

Possible targets:

```text
global component defaults
global spacing
global radius
global typography
global semantic colors
```

Lekin unnecessarily giant configuration API nahi banani.

**Minimal public API principle.**

---

# 14.12 — Existing Usage Migration

Ye separate mandatory step hoga.

Project-wide scan:

```text
pylage/
test/
app/
docs/
```

for:

```text
Style
theme
tokens
COLORS
RADIUS
SPACING
LIGHT_THEME
DARK_THEME
get_theme
```

Then classify every usage:

```text
KEEP INTERNAL
MIGRATE PUBLIC
REUSE
REMOVE
```

### Critical

Production internals may still legitimately import ENGINE classes.

Hum blindly:

```python
from pylage.ENGINE...
```

ko everywhere replace nahi karenge.

**Public-facing code/API/examples/tests → `pl.*`.**

Internal engine → internal architecture.

---

# 14.13 — Public API Tests

Dedicated Phase 14 tests.

Example:

```python
import pylage as pl

def test_root_style_api():
    assert hasattr(pl, "style")

def test_root_theme_api():
    assert hasattr(pl, "theme")

def test_set_theme():
    ...
```

Then:

```text
style presets
style merge
variants
sizes
theme lookup
global theme
custom theme
semantic colors
component overrides
global overrides
```

---

# 14.14 — Backward Compatibility / Simplicity

Principle:

> Customization must never destroy default simplicity.

So:

```python
pl.card("Hello")
```

must remain the easiest path.

Advanced:

```python
pl.card(
    "Hello",
    variant=...,
    size=...,
    style=...,
)
```

Only when needed.

No mandatory theme/style setup.

---

# 14.15 — Documentation/API Examples Migration

All user-facing examples should teach:

```python
import pylage as pl
```

not:

```python
from pylage.UI...
from pylage.ENGINE...
```

Examples should progress:

### Basic

```python
import pylage as pl

pl.card("Hello")
```

### Variant

```python
pl.button("Save", variant="primary")
```

### Style

```python
pl.card("Hello", style=pl.style.elevated_card)
```

### Theme

```python
pl.set_theme("dark")
```

---

# 14.16 — Phase 14 Full Regression

Run:

```text
Phase 14 tests
+
existing UI tests
+
full pytest
```

Expected:

```text
all existing behavior preserved
+
new customization API verified
```

No regression in default rendering.

---

# 14.17 — Tracker + Git Checkpoint

Finally:

```text
PHASE 14 [x]
```

Update only Phase 14 entries.

Then:

```text
git diff --check
git status
pytest -q
git diff
git commit
```

---

## Final Phase 14 Definition of Done

Phase 14 **tab complete nahi maana jayega** jab tak ye flow genuinely work na kare:

```python
import pylage as pl

pl.card("Hello")

pl.button(
    "Save",
    variant="primary",
    size="lg",
)

pl.card(
    "Advanced",
    style=pl.style.elevated_card,
)

pl.set_theme("dark")

pl.card("Dark themed card")
```

Aur importantly:

```text
User ko pylage.UI.*
User ko pylage.ENGINE.*
```

**jaan-ne ki zarurat nahi honi chahiye.**

### Phase 14 ka architecture

```text
                 import pylage as pl
                         │
             ┌───────────┴───────────┐
             │                       │
        Components              Customization
             │                       │
       pl.card()               pl.style
       pl.button()             pl.theme
       pl.text()               pl.set_theme()
       pl.table()              variants
             │                  sizes
             │                  overrides
             └───────────┬───────────┘
                         │
                    PyLage ENGINE
                 (internal only)
```

**Yehi Phase 14 ka complete scope hai.** Phase 15 Accessibility ko isme mix nahi karenge, aur Phase 16 Performance ko bhi nahi.

---
