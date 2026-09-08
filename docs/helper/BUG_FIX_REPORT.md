# PyLage UI Engine — Bug Tracking & Fix Log (`BUG_FIX_REPORT.md`)

This report tracks all bugs audited and resolved in the PyLage reactive UI transpiler, WebSocket state engine, component registry, and layout subsystem (`pylage` and `pylage_layout`).

Every issue follows the strict verification lifecycle:
1. **Bug Identification & Root Cause Analysis**
2. **Automated Unit & Regression Tests** in `test/`
3. **Engine Fix** (preserving all existing public API and performance contracts)
4. **Live Manual Testing Script** in `demo/`
5. **Verification**: 100% test suite pass (130 unit/integration tests)

---

## 📋 Bug Resolution Index

| Bug ID | Component / Module | Severity | Title | Test File | Manual Script | Status |
|--------|-------------------|----------|-------|-----------|---------------|--------|
| **BUG-01** | `pylage/components/basic.py` (`Accordion`) | Medium | Accordion value binding and reactive section contract | `test/test_accordion_component.py` | `demo/demo_accordion.py` | **FIXED** |
| **BUG-02** | `pylage/components/basic.py` (`Carousel`) | Medium | Carousel value / slide index reactive binding | `test/test_carousel_component.py` | `demo/demo_carousel.py` | **FIXED** |
| **BUG-03** | `pylage/core/registry.py` (`Dialog`) | Medium | Dialog boolean `open` attribute rendering without `open="False"` string artifact | `test/test_dialog_component.py` | `demo/demo_dialog.py` | **FIXED** |
| **BUG-04** | `pylage/core/registry.py` (`Drawer`) | Medium | Drawer boolean `open` attribute rendering and reactive state binding | `test/test_drawer_component.py` | `demo/demo_drawer.py` | **FIXED** |
| **BUG-05** | `pylage/core/registry.py` (`Tabs`) | Low | Tabs active value synchronization and reactive state binding | `test/test_tabs_component.py` | `demo/demo_tabs.py` | **FIXED** |
| **BUG-06** | `pylage/components/basic.py` (`DatePicker`) | Low | DatePicker value ISO binding and min/max attribute support | `test/test_datepicker_component.py` | `demo/demo_datepicker.py` | **FIXED** |
| **BUG-07** | `pylage/core/registry.py` (`Popover`, `Tooltip`, `Menu`) | Low | Popover and Tooltip prop definitions and children rendering | `test/test_popover_component.py`, `test/test_tooltip_component.py` | `demo/demo_popover_tooltip.py` | **FIXED** |
| **BUG-08** | `pylage/core/registry.py` (`Pagination`) | Low | Pagination navigation container and action buttons | `test/test_pagination_component.py` | `demo/demo_pagination.py` | **FIXED** |
| **BUG-09** | `pylage/core/events.py`, `pylage/core/binding.py`, `pylage/runtime/websocket.py` | Critical | Dynamic Subtree Indexing & JSON-safe State unwrapping after WebSocketServer start | `test/test_tree_dynamic_binding.py` | `demo/demo_accordion.py`, `demo/demo_nav_interaction.py` | **FIXED** |
| **BUG-10** | `pylage_layout/layouts/*`, `pylage_layout/tokens/*` | High | Missing layout primitives and design tokens causing import errors in `pylage_layout` | `test/test_01_tokens_audit.py`, `test/test_02_layouts_audit.py`, `test/test_03_layouts_audit.py`, `test/test_08_public_api_audit.py` | `demo/demo_layout_primitives.py`, `demo/demo_themes_tokens.py` | **FIXED** |
| **BUG-11** | `pylage/core/component.py` (`component()`) | High | Keyword collision when `type` passed in component props (`TypeError: component() got multiple values for argument 'type'`) | `test/test_component_protocol.py` | `demo/demo_table.py`, `demo/demo_data_feedback.py` | **FIXED** |
| **BUG-12** | `pylage/styling/style.py` (`Style`) | Medium | Missing standard CSS properties (`object_fit`, `object_position`, `cursor`, `overflow_x`, `overflow_y`, `aspect_ratio`, `user_select`) in `Style` dataclass | `test/test_style.py` | `demo/demo_audio_video_canvas.py` | **FIXED** |
| **BUG-13** | `pylage_layout/layouts/drawer.py` | Medium | Missing `NavigationDrawer` & `MobileSidebar` responsive factory exports | `test/test_7E_Navigation Responsiveness.py` | `demo/demo_drawer.py` | **FIXED** |
| **BUG-14** | `pylage/core/component.py` (`Component.__eq__`) | High | Reference equality vs deep attribute comparison in dynamic tree mutations (`remove`/`replace`) | `test/test_tree_remove_runtime.py`, `test/test_tree_replace_runtime.py` | `demo/demo_table.py` | **FIXED** |
| **BUG-15** | `demo/` | Feature | Missing interactive demo manuals for `pylage` components and `pylage_layout` templates/patterns | All integration test suites | `demo/demo_overview.py` + 33 dedicated manual files | **COMPLETED** |

---

## 🛠️ Detailed Bug Fix Summaries

### BUG-09: Dynamic Subtree Indexing & Reactive Binding in WebSocket Runtime
- **Issue**: Components added dynamically to the tree via `root.add(...)` or `root.replace(...)` after `WebSocketServer` initialization were not indexed by `EventDispatcher` and not bound by `StateBinding`. Additionally, serializing components containing `State` objects in `TreeAddMessage` raised `TypeError: Object of type State is not JSON serializable`.
- **Root Cause**: `EventDispatcher` and `StateBinding` only indexed nodes during their `__init__`.
- **Fix**:
  1. Added `index(node)` and `deindex(node)` to `EventDispatcher` (`pylage/core/events.py`).
  2. Added `bind(node)` to `StateBinding` (`pylage/core/binding.py`).
  3. Integrated automatic dynamic indexing, binding, and `_json_safe` prop resolution into `WebSocketServer._on_tree_mutation` for `add`, `replace`, `set_children`, `remove`, and `clear` mutations.
- **Tests Added**: `test/test_tree_dynamic_binding.py` (`test_dynamic_component_added_after_server_init_has_event_dispatch`, `test_dynamic_component_added_after_server_init_receives_state_binding`).

### BUG-10: Layout Primitives and Design Tokens in `pylage_layout`
- **Issue**: `pylage_layout` had circular imports and missing `layouts` and `tokens` packages, causing `test_01_tokens_audit.py`, `test_02_layouts_audit.py`, `test_03_layouts_audit.py`, and `test_08_public_api_audit.py` to fail.
- **Root Cause**: Missing subpackages `pylage_layout/layouts/` and `pylage_layout/tokens/`.
- **Fix**:
  1. Implemented `pylage_layout/tokens/` with `COLORS`, `FONTS`, `RADIUS`, `SPACING`, and `validate_tokens()`.
  2. Implemented `pylage_layout/layouts/` with `AppShell`, `Center`, `Container`, `Footer`, `Header`, `Navigation`, `Pagination`, `Menu`, `Section`, `SidebarLayout`, `Split`, `Stack`, `TwoColumn`, `ThreeColumn`, `Navbar`, `Topbar`, `NavigationControls`, `NavigationDrawer`, `MobileSidebar`.
- **Verification**: `01_tokens_audit: ALL PASSED`, `02_layouts_audit: ALL PASSED`, `03_layouts_audit: ALL PASSED`, `08_public_api_audit: ALL PASSED`.

### BUG-11: Component Helper Positional Parameter Collision with `type` Prop
- **Issue**: Calling `component("Alert", type="warning")` or `Alert(type="info")` raised `TypeError: component() got multiple values for argument 'type'`.
- **Root Cause**: The first positional argument in `def component(type: str, *children, **props)` was named `type`, colliding with any prop dictionary containing a `type` key (e.g. Alert type, Button type, Input type).
- **Fix**: Changed the parameter signature to `def component(type_: str, *children: Child, **props: Any) -> Component:`.
- **Verification**: All Alert, Button, and Input manuals initialize cleanly without keyword collisions.

### BUG-12: Missing CSS Properties in `Style` Dataclass
- **Issue**: Specifying standard styling properties like `object_fit`, `object_position`, `cursor`, `overflow_x`, `overflow_y`, `aspect_ratio`, `user_select`, and `text_overflow` raised `TypeError: Style.__init__() got an unexpected keyword argument`.
- **Fix**: Expanded the `Style` dataclass in `pylage/styling/style.py` to support all standard layout and rendering properties.
- **Verification**: Verified in `test_style.py` and `demo/demo_audio_video_canvas.py`.

### BUG-13: Missing `NavigationDrawer` & `MobileSidebar` in `pylage_layout.layouts.drawer`
- **Issue**: `test_7E_Navigation Responsiveness.py` failed with `ImportError: cannot import name 'NavigationDrawer' from 'pylage_layout.layouts.drawer'`.
- **Fix**: Added `NavigationDrawer`, `MobileSidebar`, and `Drawer` factory functions in `pylage_layout/layouts/drawer.py` supporting `ResponsiveStyle`.
- **Verification**: `7E FINAL RESULT: PASS` (100% assertion pass).

### BUG-03 & BUG-04: Dialog & Drawer Boolean `open` Prop Registry Contract
- **Issue**: Setting `open=False` on `Dialog` or `Drawer` rendered `<dialog open="False">` because `open` was registered as a standard attribute instead of a boolean attribute.
- **Root Cause**: `Dialog` and `Drawer` entries in `pylage/core/registry.py` were missing `"open": PropDefinition("open", kind="boolean", html_name="open")`.
- **Fix**: Added `open` boolean prop definitions to `Dialog` and `Drawer` in `pylage/core/registry.py`.
- **Tests Added**: `test/test_dialog_component.py` and `test/test_drawer_component.py`.

### BUG-01, BUG-02 & BUG-05: Accordion, Carousel & Tabs Reactive Value Prop Contract
- **Issue**: `Accordion`, `Carousel`, and `Tabs` lacked registered `value` props for binding active sections/slides/tabs dynamically.
- **Fix**: Added `"value": PropDefinition("value", kind="attribute", html_name="value")` in `pylage/components/basic.py` and `pylage/core/registry.py`.
- **Tests Added**: `test_accordion_supports_value_and_reactivity`, `test_carousel_supports_value_and_reactivity`, `test_tabs_supports_value_and_reactivity`.

---

## 🚀 Component & Layout Manual Coverage

The `demo/` suite now contains 33 comprehensive manual scripts and an interactive aggregator (`demo/demo_overview.py`):
- **Core Primitives & Inputs**: `demo_button.py`, `modern_demo_button.py`, `demo_input.py`, `demo_slider_radio_checkbox.py`, `demo_switch.py`, `demo_select.py`, `demo_datepicker.py`, `demo_form.py`
- **Structure & Layout**: `demo_column.py`, `demo_row.py`, `demo_grid.py`, `demo_card.py`, `demo_heading.py`, `demo_text.py`, `demo_avatar_badge_divider.py`, `demo_layout_primitives.py`
- **Data & Feedback**: `demo_table.py`, `demo_data_feedback.py`, `demo_accordion.py`, `demo_carousel.py`, `demo_tabs.py`, `demo_dialog.py`, `demo_drawer.py`, `demo_popover_tooltip.py`
- **Navigation & Media**: `demo_menu_breadcrumbs_pagination.py`, `demo_nav_interaction.py`, `demo_media.py`, `demo_audio_video_canvas.py`
- **Layouts & Templates**: `demo_patterns.py`, `demo_templates.py`, `demo_themes_tokens.py`, `demo_overview.py`
