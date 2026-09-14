# Installation

## Requirements

- Python **3.10+**
- `pip`
- A virtual environment is recommended

## Install from PyPI

```bash
pip install pylage
```

For development and browser testing:

```bash
pip install "pylage[test]"
```

## Verify

```bash
python -c "import pylage; print(pylage.__version__)"
```

You should see:

```text
1.0.4
```

## Development install (from source)

```bash
git clone https://github.com/aanalyst-rachit/pylage.git
cd pylage
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

## Next steps

- [First App](../first_app.md)
- [Deployment](../deployment.md)
- [Playground](https://aanalyst-rachit.github.io/pylage/playground/)
