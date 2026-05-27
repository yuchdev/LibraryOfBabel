# 03 - Source Pack Runtime Contract

## Objective

Define the stable contract consumed by `babel`.

The `babel` app must depend on this contract, not on individual external sources.

## Source Pack Directory

A source pack is a directory:

```text
babel-en-v1.sourcepack/
  manifest.json
  babel_sources.duckdb
  graph/
    semantic_graph_csr.npz
    node_index.parquet
    edge_weights.parquet
  licenses/
  checksums.sha256
```

## Required Manifest

```json
{
  "pack_id": "babel-en-v1",
  "pack_version": "1.0.0",
  "language": "en",
  "created_at": "2026-05-25T00:00:00Z",
  "schema_version": 1,
  "builder_version": "0.1.0",
  "duckdb_file": "babel_sources.duckdb",
  "features": {
    "lexical": true,
    "syntactic": true,
    "sentence_structure": true,
    "grammatical_limits": true,
    "semantic_markov": true
  },
  "counts": {
    "vocabulary_entries": 0,
    "lemmas": 0,
    "grammar_templates": 0,
    "semantic_nodes": 0,
    "semantic_edges": 0
  },
  "sources": [],
  "checksums_file": "checksums.sha256"
}
```

## Runtime Loading Rules

`babel` must support:

```bash
babel --source-pack /path/to/babel-en-v1.sourcepack
```

and environment variable:

```text
BABEL_SOURCE_PACK=/path/to/babel-en-v1.sourcepack
```

If both exist, CLI argument wins.

## Required Runtime Queries

The source pack must allow efficient runtime operations:

### Lexical Reduction

```sql
SELECT surface
FROM runtime_vocabulary
WHERE language = 'en'
ORDER BY runtime_rank;
```

### Syntactic Reduction

```sql
SELECT punctuation, class, weight
FROM punctuation_inventory
WHERE language = 'en';
```

### Sentence Structure

```sql
SELECT words_per_sentence, probability
FROM sentence_length_distribution
WHERE language = 'en' AND profile = ?;
```

### Grammatical Limits

```sql
SELECT template_id, template_json, weight
FROM grammar_templates
WHERE language = 'en' AND enabled = true;
```

### Semantic Markov

Semantic graph is loaded from:

```text
graph/semantic_graph_csr.npz
graph/node_index.parquet
```

DuckDB stores metadata and diagnostics; graph arrays store fast adjacency.

## Backward Compatibility

Until full migration:

```text
runtime_vocabulary.jsonl
```

may be used as a legacy-compatible mini-pack.

But final `babel` must prefer:

```text
sourcepack/manifest.json
```

## Versioning

Schema version and pack version are separate.

- `schema_version`: database structure.
- `pack_version`: data build version.

A patch rebuild with same schema but updated source rows increments `pack_version`, not `schema_version`.

## Integrity Validation

Before loading a source pack, `babel` must verify:

- manifest exists;
- DuckDB file exists;
- declared features match actual tables;
- checksums match;
- schema version is supported.

Failure must be explicit and actionable.

## Tests

Create runtime contract tests in `babel`:

```text
tests/integration/test_source_pack_contract.py
tests/fixtures/sourcepacks/minimal_valid/
tests/fixtures/sourcepacks/missing_manifest/
tests/fixtures/sourcepacks/bad_checksum/
```

Verify:

- valid pack loads;
- invalid pack fails with clear error;
- old `runtime_vocabulary.jsonl` fallback still works temporarily;
- model feature checks work.

