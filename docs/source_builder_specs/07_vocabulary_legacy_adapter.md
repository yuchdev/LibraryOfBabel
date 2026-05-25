# 07 — Legacy Vocabulary Adapter

## Objective

Support the existing vocabulary directory:

```text
~/.local/share/library-of-babel/vocabulary/
```

This adapter is mandatory because it allows the new source builder to be useful immediately.

## Source ID

```text
legacy_vocabulary
```

## Input Directory

Default:

```text
~/.local/share/library-of-babel/vocabulary/
```

Override:

```bash
babel-source-builder legacy scan-vocabulary --path /custom/path
```

## Supported Files

```text
*.txt
*.csv
*.json
*.jsonl
*.txt.gz
*.csv.gz
*.jsonl.gz
```

## Normalization Rules

For every input token:

1. strip whitespace;
2. lowercase by default;
3. normalize Unicode to NFKC;
4. reject empty strings;
5. reject tokens longer than configured maximum;
6. optionally reject tokens containing digits;
7. preserve original surface form.

Default config:

```toml
[legacy_vocabulary]
lowercase = true
unicode_normalization = "NFKC"
max_token_length = 64
allow_digits = false
allow_phrases = false
```

## DuckDB Export

Tables populated:

```text
source_registry
source_file
lexeme
surface_form
frequency_observation
runtime_vocabulary
```

If no rank/frequency exists, rank by:

1. file priority;
2. row order;
3. alphabetical tie-breaker.

## Runtime Compatibility Export

Must also export:

```text
~/.local/share/library-of-babel/build/runtime_vocabulary.jsonl
```

for existing `babel` runtime.

## Tests

Create:

```text
tests/unit/test_legacy_vocabulary_parser.py
tests/unit/test_legacy_vocabulary_normalization.py
tests/integration/test_legacy_vocabulary_duckdb_export.py
tests/integration/test_legacy_vocabulary_runtime_jsonl_export.py
```

## Fixture Files

```text
tests/fixtures/legacy_vocabulary/basic.txt
tests/fixtures/legacy_vocabulary/with_duplicates.txt
tests/fixtures/legacy_vocabulary/frequency.csv
tests/fixtures/legacy_vocabulary/invalid_rows.jsonl
```

## Validation

Command:

```bash
babel-source-builder source validate legacy_vocabulary
```

Checks:

- at least one token imported;
- duplicate normalized surfaces collapsed;
- `runtime_vocabulary` not empty;
- all runtime ranks unique;
- all source files have checksums.

## Exit Criteria

- old vocabulary directory is supported;
- DuckDB export works;
- legacy JSONL export works;
- `babel` can consume the output without modification after this stage.

