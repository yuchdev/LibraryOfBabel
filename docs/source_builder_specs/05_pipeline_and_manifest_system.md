# 05 - Pipeline and Manifest System

## Objective

Make all downloads and exports reproducible, inspectable, restartable, and auditable.

## Pipeline Stages

Each source adapter must support these stages:

```text
discover
download
verify
extract
import_raw_metadata
normalize
export_to_duckdb
validate
document
```

Not every source needs all stages. For example, `wordfreq` has no raw file download, but it must still record the package version and export normalized rows.

## Source Manifest

Each source gets a manifest:

```text
~/.local/share/library-of-babel/manifests/sources/<source_id>.json
```

Required fields:

```json
{
  "source_id": "wordfreq",
  "source_type": "python_package",
  "display_name": "wordfreq",
  "version": "unknown",
  "language": "en",
  "canonical_url": null,
  "license": {
    "id": null,
    "name": null,
    "url": null,
    "requires_attribution": true,
    "allows_redistribution": null
  },
  "local_files": [],
  "download": {
    "downloaded_at": null,
    "method": "python_package",
    "command": "uv add wordfreq"
  },
  "checksums": [],
  "import": {
    "imported_at": null,
    "row_count": 0
  },
  "notes": []
}
```

## Derived Manifest

Each derived artifact gets a manifest:

```text
~/.local/share/library-of-babel/manifests/derived/<artifact_id>.json
```

Example:

```json
{
  "artifact_id": "runtime_vocabulary_en_v1",
  "artifact_type": "runtime_vocabulary",
  "created_at": "2026-05-25T00:00:00Z",
  "inputs": [
    {"source_id": "legacy_vocabulary", "sha256": "..."},
    {"source_id": "wordfreq", "version": "..."}
  ],
  "output_files": [
    {
      "path": "duckdb/babel_sources.duckdb",
      "table": "runtime_vocabulary",
      "row_count": 100000
    }
  ],
  "parameters": {
    "max_words": 100000,
    "language": "en",
    "normalization": "lowercase_ascii_v1"
  }
}
```

## Source Lock File

A full build writes:

```text
~/.local/share/library-of-babel/manifests/sources.lock.json
```

This file contains exact source versions/checksums.

A source pack must include this lock file.

## Checksum Policy

Every downloaded file must have SHA-256.

If upstream does not provide checksums, compute and record local SHA-256 on first successful download.

Subsequent runs must compare the checksum unless `--refresh` is explicitly requested.

## License Policy

Every source must have a license record.

Allowed states:

```text
known_redistributable
known_non_redistributable
research_only
unknown_requires_manual_review
```

Default for unknown license:

```text
unknown_requires_manual_review
```

Source pack export must fail unless:

```bash
--allow-unknown-license
```

or the source is excluded.

## Restartability

All stages must be restartable.

Example:

```bash
babel-source-builder fetch conceptnet
```

If file already exists and checksum matches, skip download.

```bash
babel-source-builder build semantic-markov
```

If intermediate edges already exist and inputs unchanged, skip unless `--force`.

## Provenance

Every normalized row must have at least one of:

- `source_id`;
- `source_file_id`;
- `metadata_json` pointing to external source identity.

## Tests

Create:

```text
tests/unit/test_manifest_models.py
tests/unit/test_checksums.py
tests/integration/test_source_lock_reproducibility.py
tests/integration/test_unknown_license_blocks_export.py
```

## Exit Criteria

- each adapter writes source manifest;
- full build writes source lock;
- source pack includes source lock;
- checksum mismatches fail loudly;
- unknown licenses are handled explicitly.

