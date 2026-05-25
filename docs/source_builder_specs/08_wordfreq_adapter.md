# 08 — `wordfreq` Adapter

## Objective

Import common English words and frequency scores from the Python `wordfreq` package.

## Source ID

```text
wordfreq
```

## Installation

```bash
uv add wordfreq
```

## Download Stage

No raw download is required. The adapter must record:

- installed package version;
- Python environment;
- language;
- extraction parameters.

## Export Algorithm

Input:

```text
language = en
max_words = 100000
```

Algorithm:

1. import `wordfreq`;
2. call top-N word listing for English;
3. for each word:
   - normalize surface;
   - insert/update `lexeme`;
   - insert/update `surface_form`;
   - compute/record frequency values available from package;
   - insert `frequency_observation`;
4. update or rebuild `runtime_vocabulary` ranking if requested.

## DuckDB Tables

Populated:

```text
source_registry
lexeme
surface_form
frequency_observation
runtime_vocabulary
```

## Config

```toml
[wordfreq]
language = "en"
max_words = 100000
min_zipf = 0.0
include_phrases = false
```

## Unit Tests

```text
tests/unit/test_wordfreq_adapter.py
```

Test:

- adapter works when package is installed;
- max words limit respected;
- normalization is stable;
- source registry row generated.

Use monkeypatch for package calls to avoid dependency on real full list in unit tests.

## Integration Tests

```text
tests/integration/test_wordfreq_duckdb_export.py
```

Test:

- export inserts rows;
- `runtime_vocabulary` has expected number of rows;
- top words are stable enough for smoke test;
- no duplicate normalized surfaces.

## Documentation

```text
docs/sources/wordfreq.md
```

Must include:

- purpose;
- install command;
- model stages supported: Lexical, Syntactic, Sentence, Grammar, Semantic Markov as frequency prior;
- limitations;
- note about freezing package version for reproducibility.

## Exit Criteria

- source can export to DuckDB;
- source can help build runtime vocabulary;
- tests and docs exist.

