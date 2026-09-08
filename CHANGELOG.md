# Changelog


## 1.0.2 — 2026-09-08

- Corrected the published package metadata so the PyPI project description is generated from the current README.md.


## 1.0.1 — 2026-09-08

### Added

- Consolidated the development history of the PyLage, pylage-ui, pylage_layout, and pylage-ui-speed repositories into the canonical pylage repository.
- Restored the PyPI packaging configuration required for the canonical pylage package.

### Changed

- Stabilized the public PyLage API around lowercase component and helper names.
- Updated the package and public UI version to 1.0.1.
- Updated release-facing demo version labels to 1.0.1.
- Removed legacy test files from the former pylage-ui repository that were no longer compatible with the stabilized public API.

### Verification

- Full test suite: 1090 passed.
- Release verification suite: passed.
- Current release test tree matches the final pylage-ui-speed test tree: 251 Python test files.
- Working tree and release diff checks passed before release preparation.

## 1.0.0

Initial packaged PyLage release.
