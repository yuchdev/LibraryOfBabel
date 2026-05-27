# 23 - Migration Plan

## Objective

Move from legacy scattered data initialization to a unified DuckDB-backed source pack without breaking existing `babel` usage.

## Stage 0 - Inventory

Tasks:

- inspect current `babel.cli`;
- list all data initialization commands;
- list expected file paths;
- identify current vocabulary loading behavior;
- identify tests relying on old behavior.

Deliverable:

```text
docs/migration/current_data_initialization_inventory.md
```

## Stage 1 - Extract Data Initialization

Implement `babel-source-builder`.

Move commands from `babel.cli`.

Keep legacy output usable by `babel`.

Primary path:

```text
~/.local/share/library-of-babel/vocabulary/
```

Deliverable:

```text
runtime_vocabulary.jsonl
```

## Stage 2 - Add DuckDB Schema

Create schema, migrations, source registry, and legacy vocabulary export to DuckDB.

`babel` may still use JSONL, but DuckDB must exist.

## Stage 3 - Runtime Contract

Teach `babel` to load a source pack or DuckDB-backed runtime vocabulary.

Fallback order:

1. explicit source pack;
2. DuckDB source pack;
3. runtime JSONL;
4. legacy vocabulary directory with warning.

## Stage 4 - Add Source Adapters One by One

Order:

1. legacy vocabulary;
2. wordfreq;
3. NLTK;
4. Open English WordNet;
5. Universal Dependencies;
6. Project Gutenberg/SPGC;
7. Wiktionary/Kaikki;
8. ConceptNet;
9. embeddings;
10. Google Ngrams;
11. Kaggle fallbacks.

Each source must satisfy its quality gate before moving on.

## Stage 5 - Build Derived Runtime Tables

Implement:

```text
runtime_vocabulary
punctuation_inventory
sentence_length_distribution
grammar_template
semantic_transition
```

## Stage 6 - Source Pack Export

Create:

```text
babel-en-v1.sourcepack
```

`babel` loads only this pack in normal mode.

## Stage 7 - Deprecate Direct Legacy Loading

Emit warning for direct legacy directory loading.

Document:

```text
babel-source-builder legacy export-runtime-vocabulary
```

## Stage 8 - Switch Completely to DuckDB/Source Pack

`babel` default behavior:

```text
load source pack
```

Legacy path remains as an explicit import source for `babel-source-builder`, not as a runtime source for `babel`.

## Rollback Plan

At every stage, keep:

```text
runtime_vocabulary.jsonl
```

until full source pack support is stable.

Rollback command:

```bash
babel --vocabulary-file ~/.local/share/library-of-babel/build/runtime_vocabulary.jsonl
```

## Exit Criteria

Migration complete when:

- no source download/init logic remains in `babel.cli`;
- all sources export to DuckDB;
- source pack contract is stable;
- `babel` can run all five models from one source pack;
- old vocabulary directory can be imported by source builder;
- direct runtime legacy loading is deprecated or removed.

