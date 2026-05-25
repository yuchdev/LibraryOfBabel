# 24 — Definition of Done

## Full Project Completion Criteria

The project is complete when all criteria below are satisfied.

## Architecture

- `babel-source-builder` exists as a separate Python application.
- `babel.cli` no longer owns data initialization.
- `babel` loads prepared source packs.
- Legacy vocabulary directory remains importable:

```text
~/.local/share/library-of-babel/vocabulary/
```

## Sources

The following sources are accommodated into DuckDB:

- legacy vocabulary directory;
- wordfreq;
- NLTK WordNet/Brown/Gutenberg;
- Open English WordNet;
- Universal Dependencies English EWT/GUM;
- Project Gutenberg/SPGC or local Gutenberg corpus;
- Wiktionary/Kaikki;
- ConceptNet assertions;
- GloVe;
- fastText;
- ConceptNet Numberbatch;
- Google Books Ngram selected exports;
- Kaggle fallback datasets.

Each source has:

- adapter;
- download/fetch command;
- export-to-DuckDB algorithm;
- unit tests;
- integration tests;
- documentation;
- manifest entry;
- source registry entry.

## DuckDB

- schema version 1 exists;
- migrations are idempotent;
- runtime views exist;
- source registry records all sources;
- provenance is preserved;
- source lock file is generated.

## Model Exports

The source pack supports:

1. Lexical Reduction
2. Syntactic Reduction
3. Sentence Structure
4. Grammatical Limits
5. Semantic Markov

## Runtime Source Pack

A valid source pack contains:

```text
manifest.json
babel_sources.duckdb
graph/semantic_graph_csr.npz
graph/node_index.parquet
graph/edge_weights.parquet
licenses/
checksums.sha256
```

## Tests

Default CI passes:

```bash
uv run ruff check .
uv run pytest tests/unit tests/integration -m "not network and not large_data and not kaggle"
```

Optional tests exist for:

```text
network
large_data
kaggle
```

## Documentation

Docs exist for:

- architecture;
- migration;
- DuckDB schema;
- every source;
- every export algorithm;
- source pack contract;
- operations;
- troubleshooting.

## Reproducibility

The same input source lock and config must produce identical source pack checksums.

## User Experience

A fresh user can run:

```bash
babel-source-builder init
babel-source-builder fetch --preset minimal
babel-source-builder export-duckdb --preset minimal
babel-source-builder build all
babel-source-builder pack create --name babel-en-v1
babel --source-pack ~/.local/share/library-of-babel/sourcepacks/babel-en-v1.sourcepack
```

and get working generation for all five model stages, with degraded-but-functional Semantic Markov on minimal data.

