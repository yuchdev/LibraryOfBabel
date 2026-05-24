# LibraryOfBabel

This repository currently contains `babel_poc`, a local-first Python proof of concept for exploring progressively more constrained variants of Borges' Library of Babel, that models increasingly more meaningful variants of the Library.

## Dependencies and Setup

### Repository Layout

- `babel_poc/src/babel_poc` — application source code
- `babel_poc/tests` — automated tests
- `babel_poc/README.md` — detailed project usage notes and CLI examples

### Dependencies

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

### Setup

From the repository root:

```bash
cd babel
python -m pip install -e ".[dev]"
```

This installs the package in editable mode so local source changes are picked up immediately.

### Bring the App to a Working State (Vocabulary Initialization)

Most commands expect an installed vocabulary. After setup, initialize at least one source:

```bash
# Optional: inspect available sources
babel-poc vocab-list-sources

# Recommended default source
babel-poc setup-vocab --source wordfreq_25k
```

This installs vocabulary files under `~/.local/share/library-of-babel/vocabulary/`.

### Testing and Validation

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

### CI

GitHub Actions runs the test suite from `.github/workflows/ci.yml` on pushes to `main` and on pull requests. The workflow installs the package from `babel_poc/` and runs:

```bash
pytest -q
```

## Project Reference

### Mathematical Idea

The Library of Babel contains every possible book of 410 pages, each page having 40 lines of 80 characters from a 25-character alphabet. Its size is approximately 10^1,834,097.

This PoC models the library using word tokens instead of characters, exploring how different grammatical constraints affect the library's size.

### Dataset Preparation

The app will automatically look for installed vocabularies in:

```
~/.local/share/library-of-babel/vocabulary/
```

### Installing vocabularies (recommended)

```bash
# List all known vocabulary sources and their installation status
babel-poc vocab-list-sources

# Install the wordfreq top-25k English vocabulary (auto-download)
babel-poc setup-vocab --source wordfreq_25k

# Install all sources that have an automatic download URL
babel-poc setup-vocab --all

# Re-install a source (overwrite existing)
babel-poc setup-vocab --source wordfreq_25k --force
```

### Manual vocabulary

You can also pass a vocabulary file path directly on any command:

```bash
babel-poc metrics --vocab /path/to/words.txt
```

A small demo vocabulary is included at `data/vocabulary/demo.txt`.

### CLI Examples

```bash
# Show info
babel-poc info

# List known vocabulary sources
babel-poc vocab-list-sources

# Install default vocabulary (auto-download)
babel-poc setup-vocab --source wordfreq_25k

# Vocabulary statistics (uses installed vocabulary automatically)
babel-poc vocab-info

# Or with an explicit file
babel-poc vocab-info --vocab data/vocabulary/demo.txt

# Metrics for a specific mode (uses installed vocabulary)
babel-poc metrics --mode unrestricted-words

# Or with an explicit vocab file
babel-poc metrics --mode unrestricted-words --vocab data/vocabulary/demo.txt

# Generate page 3 of a deterministic book (uses installed vocabulary)
babel-poc page --mode fixed-sentence --seed "my-book" --page 3

# Compare all modes (uses installed vocabulary)
babel-poc compare
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
