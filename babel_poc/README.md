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

Place a vocabulary file at `data/vocabulary/english.txt` (one word per line).

Recommended free sources:

- **SCOWL / English Wordlist**: https://wordlist.aspell.net/
- **WordNet / Open English WordNet**: https://wordnet.princeton.edu/
- **wordfreq**: `pip install wordfreq` then export
- **Kaggle English word frequency**: https://www.kaggle.com/datasets/rtatman/english-word-frequency

A small demo vocabulary is included at `data/vocabulary/demo.txt`.

## CLI Examples

```bash
# Show info
babel-poc info

# Vocabulary statistics
babel-poc vocab-info --vocab data/vocabulary/demo.txt

# Metrics for a specific mode
babel-poc metrics --mode unrestricted-words --vocab data/vocabulary/demo.txt

# Generate page 3 of a deterministic book
babel-poc page --mode fixed-sentence --vocab data/vocabulary/demo.txt --seed "my-book" --page 3

# Compare all modes
babel-poc compare --vocab data/vocabulary/demo.txt
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
