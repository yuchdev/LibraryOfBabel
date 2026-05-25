# 21 — Documentation Requirements

## Objective

Ensure every source and derived artifact is understandable and maintainable.

## Required Top-Level Docs

```text
README.md
AGENTS.md
ARCHITECTURE.md
docs/schema/duckdb_schema_v1.md
docs/migration/from_babel_cli.md
docs/sourcepack/runtime_contract.md
docs/algorithms/semantic_markov.md
```

## Required Per-Source Docs

For each source:

```text
docs/sources/<source_id>.md
```

Template:

```markdown
# <Source Name>

## Purpose

## Models Supported

- Lexical Reduction:
- Syntactic Reduction:
- Sentence Structure:
- Grammatical Limits:
- Semantic Markov:

## Installation

## Download Command

## Local Paths

## License and Redistribution

## Exported DuckDB Tables

## Download Algorithm

## Normalization Algorithm

## Validation Algorithm

## Tests

## Expected Disk Usage

## Expected Runtime

## Known Limitations

## Troubleshooting

## Reproducibility Notes
```

## Required Algorithm Docs

```text
docs/algorithms/vocabulary_ranking.md
docs/algorithms/sentence_distribution.md
docs/algorithms/grammar_template_extraction.md
docs/algorithms/semantic_markov_graph_build.md
docs/algorithms/source_pack_export.md
```

## Required Operations Docs

```text
docs/operations/fresh_install.md
docs/operations/offline_build.md
docs/operations/rebuild_source_pack.md
docs/operations/validate_source_pack.md
docs/operations/kaggle_setup.md
docs/operations/large_data_mode.md
```

## Documentation Tests

Create:

```text
tests/unit/test_docs_source_pages_exist.py
tests/unit/test_docs_commands_parse.py
```

At minimum, verify every registered source has a matching docs page.

## Exit Criteria

- every source has docs;
- every CLI command appears in docs;
- every schema table is documented;
- every model export has an algorithm page.

