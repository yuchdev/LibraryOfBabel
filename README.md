# Library Of Babel

This repository currently contains a local-first Python application for exploring progressively more constrained variants of Borges' Library of Babel, that models increasingly more meaningful variants of the Library.

## Development Setup

### Repository Layout

- `src/babel` — application source code
- `tests` — automated tests
- `README.md` — detailed project usage notes and CLI examples

## Requirements

- Python 3.11+
- `uv`

## Install uv

macOS / Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Homebrew:

```bash
brew install uv
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Create Environment

```bash
uv sync --dev
```

## Run Application

```bash
uv run python -m babel.cli --help
```

Or:

```bash
uv run library-of-babel --help
```

## Run Tests

```bash
uv run pytest
```

## Lint and Type Check

```bash
uv run ruff check .
uv run mypy src
```

## Add Runtime Dependency

```bash
uv add package-name
```

## Add Dev Dependency

```bash
uv add --dev package-name
```

## Update Lockfile

```bash
uv lock
```

### Bring the App to a Working State (Vocabulary Initialization)

Most commands expect installed vocabulary. After setup, initialize at least one source:

```bash
# Optional: inspect available sources
uv run library-of-babel vocab-list-sources

# Recommended default source
uv run library-of-babel setup-vocab --source wordfreq_25k
```

This installs vocabulary files under `~/.local/share/library-of-babel/vocabulary/`.

### Testing and Validation (from repository root)

```bash
uv run ruff check .
uv run mypy src
uv run pytest -q
```

What each command covers:

- `uv run ruff check .` — linting and import/style checks
- `uv run mypy src` — static type checking for application code
- `uv run pytest -q` — unit and CLI smoke tests

### CI

GitHub Actions runs the test suite from `.github/workflows/ci.yml` on pushes to `main` and on pull requests. The workflow installs dependencies with uv and runs:

```bash
uv sync --dev
uv run pytest -q
```

## Project Reference

### Mathematical Idea (Article-Aligned)

- Historical Borges reference: `25^1,312,000` (documentation baseline)
- Stage 0 application baseline (English normalized): `31^1,312,000`
- Token stages use `N = 218,667` token slots/book and shared punctuation `P = 4` with:
  - punctuation alphabet: `. ? , !`

### Canonical Model Chain

| Stage | Canonical article name | App mode id | Formula | Implementation status |
|---:|---|---|---|---|
| Historical reference | Original Borges Historical Library | docs/reference only | `25^1,312,000` | Theoretical reference |
| 0 | English-Language Borges Baseline | `borges-library` | `31^1,312,000` | Implemented (canonical) |
| 1 | Lexical Reduction Model | `word-based` | `(W + P)^N` | Implemented (canonical) |
| 2 | Syntactic Reduction Model (Punctuation Constraint) | `punctuation-constrained` | `Σ binom(N-k+1,k) P^k W^(N-k)` | Implemented (canonical) |
| 3 | Sentence-Structured Uniformity Constraint | `sentence-structured` | `W^(15S) P^S`, `S=floor(N/16)` | Implemented (canonical) |
| 4 | Categorical Grammar Constraint | `grammar-constrained` | `(D·A·N·V·D·N·P)^R` | Implemented (lightweight POS fallback) |
| 5 | Markovian Semantic Adjacency Constraint | `semantic-constrained` | `≈ λ_max^N` | Implemented (lightweight deterministic graph) |
| 6 | Topic-Coherent Manifold / Topic-Constrained Vocabulary Model | `topic-coherent` | `Σ_topic (|V_topic|+P)^N` | Implemented (lightweight explicit topics) |
| 7 | Deterministic Neural Generative Steganography / Arithmetic Coding | article-only | article-only | Future/theoretical |
| 8 | Reversible Generative Flow Models | article-only | article-only | Future/theoretical |

### Theoretical vs Preview Size

- `metrics` computes full theoretical book-space sizes (fixed stage constants).
- `page` generates only the requested preview page deterministically.
- Full-book materialization is intentionally unsupported.

### Data Sources and Model Suitability

| Source | Suitable stages | Notes |
|---|---|---|
| `wordfreq_25k` | Stage 1–3, demo Stage 6 | Easy default lexical vocabulary |
| `scowl` | Stage 1–3 | Broad spelling list, not POS/semantic by default |
| `subtlex_us` | Stage 1–3 | Spoken/common vocabulary |
| `wordnet` | Stage 4–5 | POS-aware and semantic-friendly source |

### Installing vocabularies (recommended)

```bash
uv run library-of-babel vocab-list-sources
uv run library-of-babel setup-vocab --source wordfreq_25k
uv run library-of-babel setup-vocab --all
uv run library-of-babel setup-vocab --source wordfreq_25k --force
```

### Metrics Examples (all implemented modes)

```bash
uv run library-of-babel metrics --mode borges-library
uv run library-of-babel metrics --mode word-based
uv run library-of-babel metrics --mode punctuation-constrained
uv run library-of-babel metrics --mode sentence-structured
uv run library-of-babel metrics --mode grammar-constrained
uv run library-of-babel metrics --mode semantic-constrained
uv run library-of-babel metrics --mode topic-coherent
```

### Page Examples (all implemented modes)

```bash
uv run library-of-babel page --mode borges-library --seed test --page 0
uv run library-of-babel page --mode word-based --seed test --page 0
uv run library-of-babel page --mode punctuation-constrained --seed test --page 0
uv run library-of-babel page --mode sentence-structured --seed test --page 0
uv run library-of-babel page --mode grammar-constrained --seed test --page 0
uv run library-of-babel page --mode semantic-constrained --seed test --page 0
uv run library-of-babel page --mode topic-coherent --seed test --page 0
```

### Documentation and Tests

```bash
uv run ruff check .
uv run mypy src
uv run pytest -q
uv run pytest --cov=src/babel/generators --cov=src/babel/vocabulary --cov=src/babel/mathlib --cov-report=term-missing
```
