# Babel Source Builder Specification Bundle

This archive contains multiple Markdown specifications for migrating data initialization
from `babel.cli` into a new `babel-source-builder` application, progressively
accommodating all linguistic sources into a unified DuckDB database and source-pack
runtime contract.

Important path requirement:

```text
~/.local/share/library-of-babel/vocabulary/
```

is the legacy vocabulary directory and must remain supported as an import source.
