# AGENTS.md — Coding Rules for Library of Babel

## Core Rules

### 1. Local-Only Execution

Never make HTTP requests during normal execution. All vocabulary, computation, and generation must work offline.

### 2. No Full-Book Generation

Never generate all pages of a book in memory. Only generate the requested page. A book config is just metadata (seed, mode, page count).

### 3. Deterministic Generation

Use `deterministic_uint64(seed, namespace, position)` from `babel.utils.hashing`. Never use Python's `hash()` (randomized between processes) or `random.seed()` for deterministic output.

### 4. Log-Space Math
Never compute gigantic integers. Use `log10_*` functions from `babel.mathlib.logmath`.

## How to Add a New Generator Mode

1. Create `src/babel/generators/your_mode.py`
2. Implement `YourModeGenerator(LibraryGenerator)` with:
   - `mode_id: str` (kebab-case, CLI-friendly)
   - `display_name: str`
   - `log10_size(pages, tokens_per_page) -> float`
   - `generate_token(seed, position) -> str`
   - `generate_page(config, page_index) -> GeneratedPage`
3. Register in `src/babel/cli.py` → `_make_generators()`
4. Add tests in `tests/`

## Testing Rules

- Every generator must have determinism tests (same seed → same page)
- Every generator must have distinctness tests (different seed → different page)
- No-adjacent-punctuation generator must be tested for the adjacency invariant
- Fixed-sentence generator must be tested for sentence structure

## Local-Only Runtime Policy

Runtime commands (`metrics`, `page`, `compare`) must not download data unless:

* the user explicitly runs `setup-vocab`, or
* the user passes `--auto-download`.

Do not hide network access inside `metrics`, `page`, or `compare`.

Normal runtime is local-only by default (`--no-auto-download`).

Use `babel.progress.progress_context` for any operation on large data. Progress bars are transient (disappear after completion).
