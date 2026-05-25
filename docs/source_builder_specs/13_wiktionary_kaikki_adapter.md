# 13 — Wiktionary / Kaikki Adapter

## Objective

Use machine-readable Wiktionary data for broad lexical coverage, POS candidates, definitions, and morphology.

## Source ID

```text
wiktionary_kaikki_en
```

## Fetch

Default raw source path:

```text
~/.local/share/library-of-babel/sources/wiktionary_kaikki/raw-wiktextract-data.jsonl.gz
```

Command:

```bash
babel-source-builder source fetch wiktionary_kaikki_en
```

Must support:

```bash
--local-file /path/to/raw-wiktextract-data.jsonl.gz
```

## Export Algorithm

1. stream JSONL gzip line by line;
2. keep English entries;
3. extract:
   - word;
   - POS;
   - senses;
   - forms;
   - tags;
   - sounds optional;
4. normalize POS to UPOS;
5. insert lexemes and surface forms;
6. insert `lexeme_pos`;
7. insert morphological features when reliable;
8. store selected definition/sense metadata if useful;
9. skip extremely noisy or unsupported entries.

## Memory Requirement

Must stream input.

Do not load full Wiktionary into memory.

## Config

```toml
[wiktionary_kaikki]
language = "English"
max_entries = null
include_definitions = true
include_forms = true
include_multiword = false
```

## DuckDB Tables

```text
source_registry
source_file
lexeme
surface_form
lexeme_pos
morphological_feature
```

## Unit Tests

```text
tests/unit/test_kaikki_jsonl_parser.py
tests/unit/test_kaikki_pos_mapping.py
tests/unit/test_kaikki_forms_extraction.py
```

## Integration Tests

```text
tests/integration/test_kaikki_fixture_export_duckdb.py
```

Full data test marked:

```text
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/wiktionary_kaikki.md
```

Must include:

- download URL/config;
- expected size;
- streaming import algorithm;
- POS mapping table;
- known noise/limitations.

## Exit Criteria

- fixture JSONL exports;
- full file can stream without memory blow-up;
- POS/morphology rows created;
- docs and tests complete.

