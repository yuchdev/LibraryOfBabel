# LibraryOfBabel Agentic Guidelines

## Primary Goal

Make minimal, correct changes that align with the existing `babel` architecture and deterministic behavior.

## Working Agreement

1. Scope changes narrowly to the issue at hand.
2. Prefer updating existing modules over introducing new abstractions.
3. Keep runtime behavior local-first unless the user explicitly requests download/setup flows.
4. Preserve deterministic outputs for the same inputs/seeds.
5. Do not generate full books or massive combinatorial spaces in memory.

## Repository Map

- Python package: `src/babel`
- Tests: `tests`
- Repository guidance: `AGENTS.md`

## Validation

Before finishing, run from the repository root:

```bash
ruff check .
mypy src
pytest -q
```

If only documentation files changed, still verify formatting/readability and keep diffs minimal.
