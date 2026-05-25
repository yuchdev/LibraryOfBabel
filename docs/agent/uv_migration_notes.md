# UV Migration Notes

## Stage 1 Inspection Summary

- **Current dependency file(s):** `pyproject.toml` (PEP 621 + hatchling backend)
- **Current package/module name:** distribution `library-of-babel`, import package `babel` under `src/babel`
- **Current app entry point:** Typer app in `src/babel/cli.py` (`app = typer.Typer(...)`), module run supported via `python -m babel.cli`
- **Current test command:** `pytest -q`
- **Current lint/type commands:** `ruff check .`, `mypy src`
- **Minimum Python version:** `>=3.11` (`pyproject.toml`)
- **Project type:** installable package (`[build-system]` + `[project]` + console script)

## Existing Dependency Structure

`pyproject.toml` currently stores:

- Runtime dependencies in `[project.dependencies]`
- Dev tools in `[project.optional-dependencies].dev`

No `requirements.txt`, `setup.py`, `setup.cfg`, Pipenv, Poetry, or Conda files are present.

## Baseline Validation Before Migration

Executed from repository root with current workflow:

- `python -m pip install -e ".[dev]"` ✅
- `ruff check .` ❌ (pre-existing lint issues unrelated to uv migration)
- `mypy src` ❌ (pre-existing typing issues unrelated to uv migration)
- `pytest -q` ✅ (`94 passed`)

## Migration Plan

1. Keep `pyproject.toml` as source of truth and normalize dev dependencies into `[dependency-groups].dev` for uv.
2. Generate and commit `uv.lock`.
3. Make uv the primary documented workflow in `README.md` (`uv sync --dev`, `uv run ...`).
4. Update CI workflow to install and run via uv.
5. Verify with `uv sync --dev`, `uv run pytest`, and CLI help commands.

## Ambiguity Notes

- Python requirement is explicit (`>=3.11`), so it will be preserved.
- Existing console script target is `babel.cli:app`; this is retained to avoid changing CLI behavior.
