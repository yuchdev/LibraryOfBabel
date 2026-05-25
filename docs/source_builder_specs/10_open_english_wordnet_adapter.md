# 10 — Open English WordNet Adapter

## Objective

Import modern Open English WordNet data using the `wn` Python package.

## Source ID

```text
open_english_wordnet
```

## Installation

```bash
uv add wn
uv run python -m wn download oewn:2025+
```

The source builder should provide:

```bash
babel-source-builder source fetch open_english_wordnet
```

which performs the equivalent download into a controlled data directory if supported by configuration.

## Export Algorithm

1. initialize `wn`;
2. open configured WordNet project, default `oewn:2025+`;
3. iterate entries/synsets;
4. insert lemmas into `lexeme`;
5. insert surface forms;
6. insert POS candidates into `lexeme_pos`;
7. insert semantic relation edges into `semantic_edge`;
8. record synset IDs and relation names in `metadata_json`.

## POS Mapping

Use UPOS where possible:

```text
n -> NOUN
v -> VERB
a -> ADJ
r -> ADV
```

## DuckDB Tables

```text
source_registry
lexeme
surface_form
lexeme_pos
semantic_node
semantic_edge
```

## Unit Tests

```text
tests/unit/test_open_wordnet_pos_mapping.py
tests/unit/test_open_wordnet_relation_mapping.py
```

## Integration Tests

```text
tests/integration/test_open_wordnet_export_duckdb.py
```

Use tiny mocked WordNet fixture for CI by default.

Full WordNet export may be marked:

```text
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/open_english_wordnet.md
```

Must describe:

- why this source exists in addition to NLTK WordNet;
- version pinning;
- relation mapping;
- limitations for closed-class words.

## Exit Criteria

- Open English WordNet exported to DuckDB;
- WordNet relations usable by Semantic Markov;
- docs and tests complete.

