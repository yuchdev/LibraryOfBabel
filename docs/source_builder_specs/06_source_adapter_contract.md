# 06 - Source Adapter Contract

## Objective

Define a uniform Python interface for all data source adapters.

Each new source must implement this contract.

## Base Class

```python
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

class SourceAdapter(ABC):
    source_id: str
    display_name: str
    source_type: str
    language: str = "en"

    @abstractmethod
    def discover(self) -> dict:
        ...

    def download(self) -> dict:
        return {"skipped": True, "reason": "download not required"}

    def verify(self) -> dict:
        return {"verified": True}

    def extract(self) -> dict:
        return {"skipped": True, "reason": "extract not required"}

    @abstractmethod
    def export_to_duckdb(self, db_path: Path) -> dict:
        ...

    @abstractmethod
    def validate(self, db_path: Path) -> dict:
        ...

    @abstractmethod
    def documentation_context(self) -> dict:
        ...
```

## Required Adapter Metadata

Each adapter must provide:

```python
source_id
display_name
source_type
default_license
canonical_url
default_local_path
supports_incremental
supports_offline
```

## CLI Exposure

Every adapter must be invokable:

```bash
babel-source-builder source discover <source-id>
babel-source-builder source fetch <source-id>
babel-source-builder source export <source-id>
babel-source-builder source validate <source-id>
babel-source-builder source document <source-id>
```

## Adapter Output Rules

`export_to_duckdb()` must:

- open/create DuckDB database;
- ensure schema exists;
- insert/update `source_registry`;
- insert/update relevant normalized tables;
- be idempotent;
- record row counts;
- not delete unrelated source rows;
- support `--replace-source` to delete/reimport that source.

## Error Handling

Adapter failures must raise typed errors:

```python
class SourceError(Exception): ...
class SourceDownloadError(SourceError): ...
class SourceVerificationError(SourceError): ...
class SourceNormalizationError(SourceError): ...
class SourceExportError(SourceError): ...
class SourceLicenseError(SourceError): ...
```

## Testing Requirements for Every Adapter

For each adapter, create:

```text
tests/unit/test_<source>_adapter.py
tests/integration/test_<source>_export_duckdb.py
docs/sources/<source>.md
```

Unit tests must use fixtures or mocks and avoid network access.

Integration tests may use:

- tiny fixture source file;
- already installed package;
- explicit marker for large/network test.

Markers:

```text
@pytest.mark.integration
@pytest.mark.network
@pytest.mark.large_data
@pytest.mark.kaggle
```

Default CI must not run network or large-data tests.

## Documentation Requirements for Every Adapter

Each `docs/sources/<source>.md` must contain:

- purpose;
- model stages supported;
- install/download command;
- license;
- expected disk usage;
- expected import time;
- exported tables;
- validation commands;
- known limitations;
- reproducibility notes.

