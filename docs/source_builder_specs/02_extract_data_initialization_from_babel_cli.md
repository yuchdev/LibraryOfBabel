# 02 - First Mandatory Step: Extract Data Initialization from `babel.cli`

## Objective

Move all data initialization, vocabulary discovery, source downloading, and source-preparation commands from `babel.cli` into the new `babel-source-builder` application.

This must be the first implementation step.

## Rationale

The `babel` application should become a pure runtime/generation application. It should not be responsible for acquiring or preparing linguistic datasets.

During migration, the source builder must still produce data usable by `babel` **as is**, without requiring DuckDB adoption immediately.

## Existing Legacy Input

Legacy vocabularies are located at:

```text
~/.local/share/library-of-babel/vocabulary/
```

The extraction must preserve this location.

## Required Behavior

After this step:

```bash
babel-source-builder init
babel-source-builder legacy scan-vocabulary
babel-source-builder legacy export-runtime-vocabulary
```

must produce the same usable vocabulary artifacts that `babel.cli` previously created or expected.

The `babel` app must be changed to read from prepared data only.

## Required File Changes

### Create in `apps/babel-source-builder/`

```text
pyproject.toml
README.md
AGENTS.md
ARCHITECTURE.md
src/babel_source_builder/__init__.py
src/babel_source_builder/cli.py
src/babel_source_builder/config.py
src/babel_source_builder/paths.py
src/babel_source_builder/logging.py
src/babel_source_builder/sources/base.py
src/babel_source_builder/sources/legacy_vocabulary.py
src/babel_source_builder/export/legacy_runtime.py
tests/unit/test_paths.py
tests/unit/test_legacy_vocabulary_scan.py
tests/integration/test_legacy_runtime_export.py
docs/migration/legacy_data_initialization.md
```

### Edit in `apps/babel/`

```text
src/babel/cli.py
src/babel/config.py
src/babel/sourcepack/legacy_loader.py
tests/integration/test_babel_uses_legacy_export.py
README.md
```

If `sourcepack/legacy_loader.py` does not exist, create it.

## CLI Commands

### `babel-source-builder init`

Creates directory structure:

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

This command must be idempotent.

### `babel-source-builder legacy scan-vocabulary`

Scans:

```text
~/.local/share/library-of-babel/vocabulary/
```

Recognized formats:

```text
.txt
.csv
.json
.jsonl
.gz variants of the above
```

Minimum behavior:

- detect files;
- count records;
- infer format;
- compute SHA-256;
- write manifest:

```text
~/.local/share/library-of-babel/manifests/legacy_vocabulary_manifest.json
```

### `babel-source-builder legacy export-runtime-vocabulary`

Produces a normalized runtime vocabulary file compatible with current `babel`.

Suggested output:

```text
~/.local/share/library-of-babel/build/runtime_vocabulary.jsonl
```

Each row:

```json
{
  "surface": "library",
  "normalized": "library",
  "source_file": "common_words.txt",
  "source_rank": 1234,
  "source_frequency": null,
  "sha256": "..."
}
```

## `babel` Runtime Change

The existing `babel` app should no longer initialize or download data.

Instead it should look for, in order:

1. explicit `--vocabulary-file`;
2. `BABEL_VOCABULARY_FILE`;
3. `~/.local/share/library-of-babel/build/runtime_vocabulary.jsonl`;
4. legacy fallback directory `~/.local/share/library-of-babel/vocabulary/`.

The final fallback is temporary and must emit a deprecation warning:

```text
WARNING: Loading vocabulary directly from legacy directory is deprecated.
Run: babel-source-builder legacy export-runtime-vocabulary
```

## Compatibility Requirement

The generated output of `babel` for the same seed and same vocabulary ordering must remain unchanged after extraction.

If ordering changes are unavoidable, document the change and add an explicit `vocabulary_version`.

## Unit Tests

### `test_paths.py`

Verify:

- `~` expansion;
- env override;
- default paths;
- legacy vocabulary path equals `~/.local/share/library-of-babel/vocabulary/`.

### `test_legacy_vocabulary_scan.py`

Use fixture files:

```text
tests/fixtures/vocabulary/basic.txt
tests/fixtures/vocabulary/frequency.csv
tests/fixtures/vocabulary/words.jsonl
```

Verify:

- files detected;
- duplicate words handled;
- SHA-256 generated;
- invalid files skipped with warning.

## Integration Tests

### `test_legacy_runtime_export.py`

Steps:

1. create temporary data root;
2. copy fixture vocabulary files to `vocabulary/`;
3. run `babel-source-builder init`;
4. run `babel-source-builder legacy scan-vocabulary`;
5. run `babel-source-builder legacy export-runtime-vocabulary`;
6. verify `runtime_vocabulary.jsonl`;
7. verify manifest exists;
8. verify stable ordering across two runs.

### `test_babel_uses_legacy_export.py`

Steps:

1. prepare runtime vocabulary using source builder;
2. run `babel` lexical model on fixed seed;
3. verify output uses only exported vocabulary tokens;
4. verify no download command is invoked from `babel`.

## Documentation

Create:

```text
docs/migration/legacy_data_initialization.md
```

Must explain:

- why data initialization moved;
- how to run the new commands;
- how `babel` finds vocabulary;
- how to migrate existing users;
- deprecation timeline for direct legacy loading.

## Exit Criteria

This stage is complete only when:

- all data initialization commands are removed from `babel.cli` or replaced by deprecation stubs;
- `babel-source-builder` can scan and export legacy vocabulary;
- `babel` can run using exported data;
- tests pass;
- documentation exists;
- old vocabulary path remains supported.

