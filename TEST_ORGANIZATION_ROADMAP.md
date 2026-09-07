# PyLage UI Kit — Test Organization Roadmap

## Purpose

Reorganize the production v1.0.0 test suite by semantic category instead of development phase numbers. Tests must remain individually runnable by category, while the complete suite remains runnable through pytest test/.

## Current Checkpoint

- Branch: main
- Checkpoint commit: 274ac81
- Phase 16 tracker: intentionally unchanged
- Current task: Phase 16 Item 10 — production test organization and automatic regression reporting
- Test reports: permanently stored under test/reports/

## Final Test Structure

- test/foundation/ — core contracts, API, registry, style, theme, runtime foundations
- test/components/ — component and UI Kit component behavior
- test/reactive/ — state, binding, dirty-node, mutation and reactive behavior
- test/browser/ — browser and client interaction behavior
- test/websocket/ — WebSocket behavior and reactive WebSocket flows
- test/integration/ — cross-subsystem integration behavior
- test/performance/ — performance, scaling and client/bundle benchmarks
- test/regression/ — audits, compatibility, historical regression and meta-level checks
- test/reports/ — generated full-regression history

## Naming Rule

Production test filenames must describe the behavior or capability being tested. Phase numbers must not appear in test filenames or category directory names.

Examples:

test_phase16_component_creation.py -> test/performance/test_component_creation.py

test_phase16_render_overhead.py -> test/performance/test_render_overhead.py

test_phase16_large_dashboard.py -> test/performance/test_large_dashboard.py

test_phase16_large_table.py -> test/performance/test_large_table.py

test_phase16_repeated_creation.py -> test/performance/test_repeated_creation.py

test_phase16_client_bundle.py -> test/performance/test_client_bundle.py

test_phase16_state_update.py -> test/performance/test_state_update.py

test_phase16_tree_changes.py -> test/performance/test_tree_changes.py

test_phase16_websocket_update.py -> test/websocket/test_update.py

## Migration Plan

### Step 1 — Inventory

- [x] Complete current test inventory
- [x] Identify phase-based filenames
- [x] Identify component tests
- [x] Identify reactive tests
- [x] Identify browser tests
- [x] Identify WebSocket tests
- [x] Identify performance tests
- [x] Identify audit and regression tests

### Step 2 — Validate Mapping

- [x] Inspect ambiguous test contents
- [x] Confirm final category for every test file
- [x] Confirm no test is duplicated or lost

### Step 3 — Create Category Structure

- [x] Create foundation/
- [x] Create components/
- [x] Create reactive/
- [x] Create browser/
- [x] Create websocket/
- [x] Create integration/
- [x] Create performance/
- [x] Create regression/
- [x] Create reports/

### Step 4 — Rename and Move Tests

- [x] Remove phase numbers from production test filenames
- [x] Move tests into semantic categories
- [x] Preserve all existing test code
- [x] Preserve temporary regression tests
- [x] Verify pytest discovery

### Step 5 — Selective Execution

- [x] pytest test/foundation/
- [x] pytest test/components/
- [x] pytest test/reactive/
- [x] pytest test/browser/
- [x] pytest test/websocket/
- [x] pytest test/integration/
- [x] pytest test/performance/
- [x] pytest test/regression/
- [x] pytest test/

### Step 6 — Automatic Regression Reporting

- [x] Generate report automatically after full pytest test/ execution
- [x] Store report permanently under test/reports/
- [x] Record timestamp
- [x] Record commit SHA
- [x] Record branch
- [x] Record total duration
- [x] Record total/passed/failed/skipped counts
- [x] Record category-wise results
- [x] Record key highlights
- [x] Record performance highlights
- [x] Record final PASS/FAIL status

### Step 7 — Validation

- [x] Run every category independently
- [x] Verify category isolation
- [x] Run full regression
- [x] Verify automatic report creation
- [x] Verify report contains correct commit and test totals
- [x] Verify no tests were lost during migration
- [x] Verify git diff is clean except intentional changes

### Step 8 — Phase 16 Completion

- [x] Complete Item 10
- [x] Run one final full regression
- [x] Update PYSKIN/PyLage UI Kit Phase 16 tracker only after all checks pass
- [ ] Commit final Phase 16 work
- [ ] Push final Phase 16 work

## Reporting Format

The full regression report should contain:

TEST REGRESSION REPORT

Run Date
Commit
Branch
Overall Result
Total Tests
Passed
Failed
Skipped
Duration

CATEGORY SUMMARY

Category
Tests
Passed
Failed
Skipped
Duration

KEY HIGHLIGHTS

Important passing checks, failures, skipped tests and notable production verification points.

PERFORMANCE HIGHLIGHTS

Component creation, render overhead, state updates, WebSocket behavior, large dashboard, large table, repeated creation and client runtime/bundle checks.

END OF REPORT

## Progress Tracking Rule

This roadmap is the persistent working record for test organization. Each completed migration or reporting step must be checked here. Phase 16 itself remains incomplete until Item 10 and all previous Phase 16 items have been verified together.
