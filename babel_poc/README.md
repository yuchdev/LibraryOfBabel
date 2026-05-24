# Library of Babel — Local Python PoC

A local-only Python proof-of-concept that models progressively more meaningful variants of Borges' Library of Babel.

## Mathematical Idea

The Library of Babel contains every possible book of 410 pages, each page having 40 lines of 80 characters from a 25-character alphabet. Its size is approximately 10^1,834,097.

This PoC models the library using word tokens instead of characters, exploring how different grammatical constraints affect the library's size.

## Installation

```bash
cd babel_poc
pip install -e ".[dev]"
```

## Dataset Preparation

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

## CLI Examples

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

## Implemented Modes

| Mode | Formula | Description |
|------|---------|-------------|
| `unrestricted-words` | (W+P)^N | Any token at any position |
| `no-adjacent-punctuation` | Σ C(N-k+1,k)·P^k·W^(N-k) | No two punctuation marks in a row |
| `fixed-sentence` | W^(S·w)·P^S | Fixed-length sentences |
| `pos-template` | Π(category_size)^repetitions | Follows POS pattern |

## Known Limitations

- POS-template mode uses a tiny built-in vocabulary
- No-adjacent-punctuation log10_size uses log-space summation (may be slow for very large N)
- Full-book generation is intentionally unsupported

## Future SPA Migration

This PoC serves as the mathematical reference for a React/TypeScript SPA. The generator interfaces map directly to TypeScript classes.
