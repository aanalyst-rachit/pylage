# Installation

## Definition

PyLage is currently developed and verified from this repository as the `pylage` Python package.

The final updated PyLage release is planned for publication on PyPI after the documentation phase is complete.

## Requirements

- Python 3.12 is verified in the current development environment.
- A Python virtual environment is recommended for project isolation.
- `pip` is required for Python package installation workflows.

## Development Setup

Create and activate the project virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Repository Verification

The current repository can be verified directly from the project checkout:

```bash
python -c "import pylage; print(pylage.__file__)"
```

A successful check confirms that the current repository package can be imported.

## Current PyPI Package

The `pylage` package currently available on PyPI is an older demo release that was published to reserve the package name and URL.

It should not be treated as the current repository release or as the source of the current PyLage implementation.

The updated repository version will be published to PyPI after the documentation work is completed.

## Packaging Status

This repository currently does not contain `pyproject.toml`, `setup.py`, or `setup.cfg`.

Therefore, the documentation does not prescribe `pip install -e .` or another repository installation command that depends on packaging metadata.

For current development, use the repository checkout and its virtual environment.

## API Boundary

Application code imports the package as:

```python
import pylage as pl
```

## Verification

The current development checkout was verified with Python 3.12.3 and a successful `import pylage`.

The separately installed PyPI `pylage` package was verified as an older demo release and is intentionally distinguished from the current repository version.

## Verified Sources

- `README.MD` — existing project quick-start and installation references.
- `pylage/__init__.py` — current package root.
- Current repository package import verification.

## Status

Installation documentation reflects the current repository workflow and clearly distinguishes the legacy/demo PyPI package from the upcoming updated PyLage release.
