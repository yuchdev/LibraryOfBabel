# LibraryOfBabel

This repository currently contains `babel_poc`, a local-first Python proof of concept for exploring progressively more constrained variants of Borges' Library of Babel.

## Repository Layout

- `babel_poc/src/babel_poc` — application source code
- `babel_poc/tests` — automated tests
- `babel_poc/README.md` — detailed project usage notes and CLI examples

## Dependencies

The `babel_poc` package targets **Python 3.11+** and is defined in `babel_poc/pyproject.toml`.

### Runtime dependencies

- `typer>=0.12`
- `rich>=13.0`
- `pydantic>=2.0`
- `numpy>=1.26`
- `scipy>=1.12`

### Development dependencies

- `pytest>=8.0`
- `ruff>=0.6`
- `mypy>=1.10`

Install everything, including development tools, with the editable setup below.

## Setup

From the repository root:

```bash
cd babel_poc
python -m pip install -e ".[dev]"
```

This installs the package in editable mode so local source changes are picked up immediately.

## Testing and Validation

Run all validation commands from the `babel_poc/` directory:

```bash
ruff check .
mypy src
pytest -q
```

What each command covers:

- `ruff check .` — linting and import/style checks
- `mypy src` — static type checking for application code
- `pytest -q` — unit and CLI smoke tests

## CI

GitHub Actions runs the test suite from `.github/workflows/ci.yml` on pushes to `main` and on pull requests. The workflow installs the package from `babel_poc/` and runs:

```bash
pytest -q
```

## Additional Project Documentation

For installation details, vocabulary setup, implemented modes, and CLI examples, see:

- `babel_poc/README.md`
