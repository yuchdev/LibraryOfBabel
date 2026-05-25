# 01 — Project Architecture

## Objective

Create a standalone Python application named `babel-source-builder` that owns all data initialization, downloading, normalization, source accommodation, and DuckDB export.

The existing `babel` app must become a consumer of prepared source packs only.

## Repository Layout

Recommended repository layout:

```text
library-of-babel/
  apps/
    babel/
      src/babel/
        cli.py
        models/
        sourcepack/
      tests/

    babel-source-builder/
      pyproject.toml
      README.md
      AGENTS.md
      ARCHITECTURE.md
      src/babel_source_builder/
        __init__.py
        cli.py
        config.py
        paths.py
        logging.py
        db/
          connection.py
          schema.py
          migrations/
        manifest/
          models.py
          read_write.py
          checksums.py
        sources/
          base.py
          legacy_vocabulary.py
          wordfreq_source.py
          nltk_source.py
          open_wordnet_source.py
          universal_dependencies_source.py
          gutenberg_source.py
          kaikki_source.py
          conceptnet_source.py
          embeddings_source.py
          google_ngrams_source.py
          kaggle_source.py
        normalize/
          tokens.py
          lemmas.py
          pos.py
          morphology.py
          sentences.py
          provenance.py
        export/
          vocabulary.py
          syntax.py
          sentence.py
          grammar.py
          semantic_markov.py
          sourcepack.py
        qa/
          db_assertions.py
          sample_data.py
      tests/
        unit/
        integration/
        fixtures/
        snapshots/
      docs/
        sources/
        schema/
        algorithms/
        migration/
```

If the project is not a monorepo, the same structure can be used in two repositories:

```text
library-of-babel
library-of-babel-source-builder
```

## Runtime Separation

### `babel-source-builder`

Responsibilities:

- know external source URLs;
- know Kaggle dataset slugs;
- download raw sources;
- verify hashes;
- unpack archives;
- normalize tokens, lemmas, POS tags, morphology, sentences, and semantic edges;
- create and migrate DuckDB schema;
- export source packs;
- document provenance and licenses.

### `babel`

Responsibilities:

- load source pack metadata;
- load vocabulary tables;
- load grammar templates;
- load semantic graph arrays;
- generate pages deterministically;
- display metrics;
- never download external sources during normal generation.

## Data Roots

Default data root:

```text
~/.local/share/library-of-babel/
```

Required subdirectories:

```text
~/.local/share/library-of-babel/
  vocabulary/
  sources/
  build/
  duckdb/
  sourcepacks/
  manifests/
  logs/
```

The legacy vocabulary location is mandatory:

```text
~/.local/share/library-of-babel/vocabulary/
```

## Configuration Precedence

Configuration values must be resolved in this order:

1. CLI argument
2. Environment variable
3. Project config file
4. User config file
5. Built-in default

Example:

```text
--data-root
BABEL_DATA_HOME
./babel-source-builder.toml
~/.config/library-of-babel/source-builder.toml
~/.local/share/library-of-babel
```

## Main Configuration Keys

```toml
[data]
root = "~/.local/share/library-of-babel"
legacy_vocabulary_dir = "~/.local/share/library-of-babel/vocabulary"
sources_dir = "~/.local/share/library-of-babel/sources"
build_dir = "~/.local/share/library-of-babel/build"
duckdb_path = "~/.local/share/library-of-babel/duckdb/babel_sources.duckdb"
sourcepacks_dir = "~/.local/share/library-of-babel/sourcepacks"

[network]
enabled = true
timeout_seconds = 60
retries = 3

[kaggle]
enabled = false

[export]
language = "en"
pack_name = "babel-en-v1"
```

## Logging

All commands must log to:

```text
~/.local/share/library-of-babel/logs/source-builder.log
```

The CLI must also emit concise progress information to stdout.

Log levels:

- `DEBUG`: row-level diagnostics only when explicitly requested.
- `INFO`: source found, download started, download completed, normalization completed.
- `WARNING`: optional source unavailable, fallback used, license unknown.
- `ERROR`: invalid schema, checksum mismatch, corrupt archive, failed export.
- `CRITICAL`: database migration failure, destructive operation refused.

## Exit Codes

```text
0  success
1  generic failure
2  invalid CLI/config
3  source unavailable
4  checksum/license failure
5  schema validation failure
6  test/QA failure
7  export failure
8  migration failure
```

## Agentic Development Rules

Each implementation task must list:

- files to create;
- files to edit;
- unit tests;
- integration tests;
- documentation files;
- exit criteria.

If an agent returns a result without the expected files, launch a correction iteration and explicitly compare against the file list.

