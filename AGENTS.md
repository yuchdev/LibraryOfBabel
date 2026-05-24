# AGENTS.md — Repository Guidelines

## Scope

This repository currently contains the `babel_poc` Python project.

## Project Location

- Main code: `babel_poc/src/babel_poc`
- Tests: `babel_poc/tests`

## Local Development

```bash
cd babel_poc
pip install -e ".[dev]"
```

## Validation Commands

Run from `babel_poc/`:

```bash
ruff check .
mypy src
pytest -q
```

## Implementation Rules

- Keep runtime local-first by default (no hidden network access in normal runtime commands).
- Preserve deterministic generation behavior across runs.
- Avoid materializing huge search spaces in memory; generate only what is requested.
- Prefer small, surgical changes with focused tests when behavior changes.
