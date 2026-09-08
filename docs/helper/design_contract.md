# PyLage UI Kit — Design Contract

## 1. Scope

The UI Kit is the high-level developer experience layer of PyLage. It provides semantic component defaults, composition conventions, responsive defaults, interaction-state conventions, and reusable UI recipes while reusing the existing PyLage styling, theme, token, layout, state, and rendering infrastructure.

## 2. Architecture Boundary

The UI Kit MUST NOT introduce a second rendering engine, reactive state engine, WebSocket protocol, DOM patching system, CSS engine, theme engine, token engine, or layout engine.

The intended dependency direction is:

    pylage_ui
        ↓
    existing PyLage APIs
        ↓
    pylage / pylage_layout

## 3. Spacing

- Reuse the existing pylage_layout SPACING tokens.
- Component defaults MUST select semantic spacing values rather than inventing arbitrary values.
- The existing spacing scale is xs, sm, md, lg, xl, 2xl, 3xl, and 4xl, plus 0.
- Custom spacing remains possible through the existing Style API.

## 4. Radius

- Reuse the existing RADIUS token scale.
- Components MUST choose consistent semantic radius defaults.
- The existing scale is none, sm, md, lg, xl, 2xl, and full.
- Custom radius remains possible through Style.

## 5. Typography

- Reuse the existing Theme font system and FONTS tokens.
- The UI Kit may define semantic typography roles such as heading, body, label, caption, and metric.
- Typography roles are conventions, not a second typography engine.
- Component-specific typography MUST remain overridable through Style.

## 6. Surfaces and Borders

- Reuse existing semantic surface tokens: background, surface, and surface_variant.
- Reuse existing border and border_muted tokens.
- Components MUST prefer semantic tokens over hard-coded colors.
- Existing Style remains the mechanism for applying the resulting CSS.

## 7. Semantic Colors

- Reuse the existing semantic color vocabulary.
- Supported semantic roles include primary, secondary, success, warning, danger, and info.
- Primary and secondary hover and contrast tokens MUST be reused where applicable.
- The UI Kit MUST NOT create a parallel color registry.

## 8. Shadows

- Reuse Style.box_shadow for shadow application.
- The UI Kit may define semantic shadow presets as component conventions if required.
- No separate shadow engine or CSS generation system is permitted.

## 9. Interaction States

### Hover

- Interactive components SHOULD provide a consistent hover treatment.
- Existing semantic hover tokens SHOULD be reused where available.

### Focus

- Interactive components MUST expose a visible focus state.
- Focus styling MUST remain compatible with keyboard navigation and accessibility requirements.

### Disabled

- Disabled components MUST provide a visually distinguishable disabled state.
- Disabled state styling MUST prevent misleading interactive affordances.

## 10. Responsive Defaults

- Reuse ResponsiveStyle.
- Reuse the existing breakpoints: sm 640px, md 768px, lg 1024px, and xl 1280px.
- Components and recipes MAY provide responsive defaults.
- The UI Kit MUST NOT introduce a competing breakpoint or responsive engine.
- Explicit ResponsiveStyle and Style customization remain available to developers.

## 11. Customization

- UI Kit defaults are conventions, not restrictions.
- Existing Style is the primary low-level customization mechanism.
- Existing Theme remains the theme abstraction.
- Existing custom CSS properties through Style.custom remain available.
- UI Kit components SHOULD allow sensible style overrides without requiring users to bypass the UI Kit entirely.

## 12. Composition

- UI Kit components SHOULD compose existing PyLage primitives.
- UI Kit recipes SHOULD compose existing pylage_layout layouts, patterns, and templates.
- Existing components MUST be wrapped or composed before considering new primitives.
- BUILD is permitted only when the required capability genuinely does not exist.

## 13. Implementation Rules

For every UI Kit capability, use this order:

1. Inspect existing PyLage functionality.
2. Classify the capability as REUSE, WRAP, COMPOSE, or BUILD.
3. Prefer REUSE over WRAP.
4. Prefer WRAP/COMPOSE over BUILD.
5. Implement only the missing UI Kit layer.
6. Add focused tests.
7. Run the relevant test suite and full regression suite.

## 14. Source of Truth

This document defines the Phase 03 UI Kit design contract. Later implementation phases MUST follow these boundaries unless the contract is deliberately revised and recorded in the project tracker.
