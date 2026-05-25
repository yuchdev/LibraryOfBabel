# 22 — CLI Specification

## Objective

Define stable CLI commands for `babel-source-builder`.

## Global Options

```bash
babel-source-builder \
  --data-root ~/.local/share/library-of-babel \
  --config ./babel-source-builder.toml \
  --log-level INFO \
  <command>
```

## Commands

### Init

```bash
babel-source-builder init
```

Creates directory structure and default config.

### Source Discovery

```bash
babel-source-builder source list
babel-source-builder source discover <source-id>
```

### Fetch

```bash
babel-source-builder source fetch <source-id>
babel-source-builder fetch --preset minimal
babel-source-builder fetch --preset full
```

Presets:

```text
minimal:
  legacy_vocabulary
  wordfreq
  nltk
  ud_english_ewt

full:
  legacy_vocabulary
  wordfreq
  nltk
  open_english_wordnet
  ud_english_ewt
  ud_english_gum
  project_gutenberg_spgc
  wiktionary_kaikki_en
  conceptnet_assertions
  glove_6b
  fasttext_crawl_300d
  conceptnet_numberbatch
  google_books_1grams
  google_books_2grams
```

Kaggle is never enabled by default.

### Export Source to DuckDB

```bash
babel-source-builder source export <source-id>
babel-source-builder export-duckdb --preset minimal
babel-source-builder export-duckdb --preset full
```

### Build Derived Artifacts

```bash
babel-source-builder build vocabulary
babel-source-builder build syntax
babel-source-builder build sentence
babel-source-builder build grammar
babel-source-builder build semantic-markov
babel-source-builder build all
```

### Validate

```bash
babel-source-builder validate db
babel-source-builder validate source <source-id>
babel-source-builder validate sourcepack /path/to/sourcepack
```

### Pack

```bash
babel-source-builder pack create --name babel-en-v1
babel-source-builder pack verify ~/.local/share/library-of-babel/sourcepacks/babel-en-v1.sourcepack
```

### Legacy Compatibility

```bash
babel-source-builder legacy scan-vocabulary
babel-source-builder legacy export-runtime-vocabulary
```

### QA

```bash
babel-source-builder qa assert-db --db path.duckdb --spec expected.json
```

## Command Output

Every long command must emit:

- stage name;
- progress;
- output path;
- rows processed;
- warnings;
- next suggested command.

Example:

```text
[INFO] Exported source wordfreq
Rows inserted:
  lexeme: 100000
  surface_form: 100000
  frequency_observation: 100000
Next:
  babel-source-builder build vocabulary
```

## Tests

```text
tests/unit/test_cli_help.py
tests/integration/test_cli_init.py
tests/integration/test_cli_minimal_pipeline.py
```

## Exit Criteria

- CLI help works;
- all commands are documented;
- minimal pipeline can run from CLI in temp directory;
- invalid commands fail with useful messages.

