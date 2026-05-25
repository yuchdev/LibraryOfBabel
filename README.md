# LibraryOfBabel

This repository currently contains a local-first Python proof of concept for exploring progressively more constrained variants of Borges' Library of Babel, that models increasingly more meaningful variants of the Library.

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

### Mathematical Idea

The Library of Babel contains every possible book of 410 pages, each page having 40 lines of 80 characters from a 25-character alphabet. Its size is approximately 10^1,834,097.

This PoC models the library using word tokens instead of characters, exploring how different grammatical constraints affect the library's size.

See the detailed model description in [docs/Semantic_Models_of_Library_of_Babel_teaser.md](docs/Semantic_Models_of_Library_of_Babel_teaser.md).

### Dataset Preparation

The app will automatically look for installed vocabularies in:

```
~/.local/share/library-of-babel/vocabulary/
```

### Installing vocabularies (recommended)

```bash
# List all known vocabulary sources and their installation status
uv run library-of-babel vocab-list-sources

# Install the wordfreq top-25k English vocabulary (auto-download)
uv run library-of-babel setup-vocab --source wordfreq_25k

# Install all sources that have an automatic download URL
uv run library-of-babel setup-vocab --all

# Re-install a source (overwrite existing)
uv run library-of-babel setup-vocab --source wordfreq_25k --force
```

### Manual vocabulary

You can also pass a vocabulary file path directly on any command:

```bash
uv run library-of-babel metrics --vocab /path/to/words.txt
```

A small demo vocabulary is included at `data/vocabulary/demo.txt`.

### CLI Examples

```bash
# Show info
uv run library-of-babel info

# List known vocabulary sources
uv run library-of-babel vocab-list-sources

# Install default vocabulary (auto-download)
uv run library-of-babel setup-vocab --source wordfreq_25k

# Vocabulary statistics (uses installed vocabulary automatically)
uv run library-of-babel vocab-info

# Or with an explicit file
uv run library-of-babel vocab-info --vocab data/vocabulary/demo.txt

# Metrics for a specific mode (uses installed vocabulary)
uv run library-of-babel metrics --mode unrestricted-words

# Or with an explicit vocab file
uv run library-of-babel metrics --mode unrestricted-words --vocab data/vocabulary/demo.txt

# Generate page 3 of a deterministic book (uses installed vocabulary)
uv run library-of-babel page --mode fixed-sentence --seed "my-book" --page 3

# Compare all modes (uses installed vocabulary)
uv run library-of-babel compare
```

### Implemented Modes

| Mode                      | Formula                      | Description                       |
|---------------------------|------------------------------|-----------------------------------|
| `unrestricted-words`      | (W+P)^N                      | Any token at any position         |
| `no-adjacent-punctuation` | Σ C(N-k+1,k)·P^k·W^(N-k)     | No two punctuation marks in a row |
| `fixed-sentence`          | W^(S·w)·P^S                  | Fixed-length sentences            |
| `pos-template`            | Π(category_size)^repetitions | Follows POS pattern               |

### Known Limitations

- POS-template mode uses tiny built-in vocabulary
- No-adjacent-punctuation `log10_size` uses log-space summation (maybe slow for a very large `N`)
- Full-book generation is intentionally unsupported
