# 20 — Tests and Quality Gates

## Objective

Define testing strategy for a large data-heavy research project.

## Test Categories

### Unit Tests

Fast, no network, no large files.

```bash
uv run pytest tests/unit
```

### Integration Tests

Use tiny fixture files and temporary DuckDB databases.

```bash
uv run pytest tests/integration
```

### Network Tests

Explicitly marked and skipped by default.

```bash
uv run pytest -m network
```

### Large Data Tests

Explicitly marked and skipped by default.

```bash
uv run pytest -m large_data
```

### Kaggle Tests

Explicitly marked and skipped by default.

```bash
uv run pytest -m kaggle
```

## Required Pytest Markers

```ini
[pytest]
markers =
    integration: integration tests
    network: requires network
    large_data: requires large local datasets
    kaggle: requires Kaggle credentials
    slow: slow tests
```

## Fixture Strategy

Create tiny versions of every source:

```text
tests/fixtures/
  legacy_vocabulary/
  nltk_like/
  ud/
  gutenberg/
  kaikki/
  conceptnet/
  embeddings/
  google_ngrams/
  kaggle/
```

## Golden Snapshot Tests

Snapshot outputs:

```text
tests/snapshots/
  runtime_vocabulary_expected.jsonl
  grammar_templates_expected.json
  semantic_graph_stats_expected.json
```

Snapshot tests must allow intentional update only via:

```bash
UPDATE_SNAPSHOTS=1 uv run pytest
```

## Reproducibility Tests

Required:

```text
test_rebuild_same_inputs_same_checksums
test_source_lock_blocks_unexpected_change
test_pack_manifest_reproduces_artifact_list
```

## Database QA Helper

Create:

```text
src/babel_source_builder/qa/db_assertions.py
```

CLI:

```bash
babel-source-builder qa assert-db --db path.duckdb --spec expected.json
```

JSON example:

```json
{
  "tables": {
    "runtime_vocabulary": {
      "min_rows": 10,
      "required_columns": ["runtime_rank", "surface", "score"]
    },
    "grammar_template": {
      "min_rows": 1
    }
  },
  "queries": [
    {
      "name": "no duplicate runtime ranks",
      "sql": "SELECT COUNT(*) FROM (SELECT runtime_rank, COUNT(*) c FROM runtime_vocabulary GROUP BY runtime_rank HAVING c > 1)",
      "expect_scalar": 0
    }
  ]
}
```

## CI

Default CI must run:

```bash
uv run ruff check .
uv run pytest tests/unit tests/integration -m "not network and not large_data and not kaggle"
```

Optional scheduled CI may run network tests.

## Quality Gates Per Source

A source cannot be considered accommodated unless:

- adapter exists;
- docs exist;
- unit tests exist;
- integration fixture test exists;
- DuckDB export works;
- source manifest is written;
- source registry row exists;
- validation command passes.

## Quality Gates Per Export

An export cannot be considered complete unless:

- deterministic output;
- manifest updated;
- checksum generated;
- runtime contract test passes;
- docs updated.

