# 17 - Kaggle Adapter

## Objective

Support Kaggle as a fallback/mirror source provider.

Kaggle must not be the default canonical provider when official/canonical sources are available.

## Source ID Pattern

```text
kaggle_<owner>_<dataset>
```

Examples:

```text
kaggle_rtatman_english_word_frequency
kaggle_mateibejan_15000_gutenberg_books
kaggle_conceptnet_assertions
```

## Installation

```bash
uv add kaggle
```

## Authentication

The adapter must not assume credentials exist.

Supported auth methods:

```text
kaggle auth login
~/.kaggle/kaggle.json
KAGGLE_USERNAME + KAGGLE_KEY
```

## Dataset Registry

Create:

```text
src/babel_source_builder/sources/kaggle_registry.py
```

Example registry row:

```python
{
    "source_id": "kaggle_rtatman_english_word_frequency",
    "owner_slug": "rtatman",
    "dataset_slug": "english-word-frequency",
    "maps_to": "frequency",
    "canonical_replacement": "wordfreq/google_ngrams",
    "default_enabled": False,
}
```

## Fetch Algorithm

1. verify Kaggle auth;
2. download dataset zip;
3. compute checksum;
4. unzip into dataset-specific directory;
5. scan files;
6. call appropriate importer:
   - frequency CSV importer;
   - Gutenberg corpus importer;
   - embedding importer;
   - ConceptNet importer.

## DuckDB Export

Kaggle adapter itself inserts source metadata into:

```text
source_registry
source_file
```

Then delegates to typed importers.

## Tests

Unit:

```text
tests/unit/test_kaggle_registry.py
tests/unit/test_kaggle_command_builder.py
tests/unit/test_kaggle_dataset_mapping.py
```

Integration:

```text
tests/integration/test_kaggle_fixture_zip_import.py
```

Network tests:

```text
@pytest.mark.kaggle
@pytest.mark.network
```

## Documentation

```text
docs/sources/kaggle.md
```

Must include:

- auth setup;
- supported dataset registry;
- fallback role;
- license warning;
- how to add a new Kaggle dataset.

## Exit Criteria

- Kaggle datasets can be registered declaratively;
- fixture zip import works;
- unsupported Kaggle dataset fails clearly;
- docs and tests complete.

