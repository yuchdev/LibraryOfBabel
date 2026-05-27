# Library of Babel Source Builder - Specification Index

## Purpose

This specification set defines a staged migration from data-initialization logic embedded in `babel.cli` into a separate Python application responsible for downloading, normalizing, validating, and exporting all linguistic data sources required by the Library of Babel research application.

The new application is tentatively named:

```text
babel-source-builder
```

The existing generation application is referred to as:

```text
babel
```

## Strategic Goal

The final architecture must separate responsibilities:

```text
babel-source-builder
  Downloads external sources.
  Normalizes them.
  Accommodates them into a unified DuckDB database.
  Exports source packs usable by babel.

babel
  Does not download or parse external research sources.
  Loads one prepared source pack.
  Runs deterministic generation models.
```

## Critical User Constraint

Existing vocabulary files are located in:

```text
~/.local/share/library-of-babel/vocabulary/
```

This path must be treated as the legacy default vocabulary directory during migration.

## Documents

| Document | Purpose |
|---|---|
| `00_index.md` | This index |
| `01_project_architecture.md` | Overall architecture and repository layout |
| `02_extract_data_initialization_from_babel_cli.md` | First mandatory migration step |
| `03_source_pack_runtime_contract.md` | Contract between `babel-source-builder` and `babel` |
| `04_duckdb_schema_v1.md` | Unified DuckDB schema |
| `05_pipeline_and_manifest_system.md` | Reproducibility, manifests, checksums, source locks |
| `06_source_adapter_contract.md` | Common interface for every source adapter |
| `07_vocabulary_legacy_adapter.md` | Adapter for `~/.local/share/library-of-babel/vocabulary/` |
| `08_wordfreq_adapter.md` | `wordfreq` source integration |
| `09_nltk_adapter.md` | NLTK WordNet/Brown/Gutenberg integration |
| `10_open_english_wordnet_adapter.md` | Open English WordNet via `wn` |
| `11_universal_dependencies_adapter.md` | UD English EWT/GUM integration |
| `12_project_gutenberg_adapter.md` | Project Gutenberg / SPGC integration |
| `13_wiktionary_kaikki_adapter.md` | Wiktionary/Kaikki integration |
| `14_conceptnet_adapter.md` | ConceptNet assertions integration |
| `15_embeddings_adapter.md` | GloVe, fastText, Numberbatch integration |
| `16_google_ngrams_adapter.md` | Google Books Ngram integration |
| `17_kaggle_adapter.md` | Kaggle fallback/mirror integration |
| `18_export_algorithms_by_model.md` | Derived exports for models 1–5 |
| `19_semantic_markov_graph_build.md` | Semantic Markov graph build algorithm |
| `20_tests_and_quality_gates.md` | Unit, integration, snapshot, reproducibility tests |
| `21_documentation_requirements.md` | Documentation requirements for each source |
| `22_cli_specification.md` | CLI commands and expected behavior |
| `23_migration_plan.md` | Migration stages from legacy data sources to DuckDB |
| `24_definition_of_done.md` | Exit criteria for the full project |

## Model Coverage

The source builder must support the first five Library of Babel models:

1. Lexical Reduction
2. Syntactic Reduction
3. Sentence Structure
4. Grammatical Limits
5. Semantic Markov

## Non-Goals

The source builder must not:

- generate Library pages directly;
- contain UI code;
- require the `babel` app to know external source internals;
- silently download unlicensed or unknown-license data;
- silently mutate existing legacy vocabulary files;
- require network access at runtime in `babel`.

## High-Level Final State

```text
~/.local/share/library-of-babel/
  vocabulary/
    legacy vocabulary files, preserved

  sources/
    raw external downloads

  build/
    temporary normalized/intermediate files

  duckdb/
    babel_sources.duckdb

  sourcepacks/
    babel-en-v1/
      manifest.json
      babel_sources.duckdb
      semantic_graph_csr.npz
      checksums.sha256
      licenses/
```

