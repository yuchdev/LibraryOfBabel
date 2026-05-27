# 14 - ConceptNet Adapter

## Objective

Import ConceptNet assertions as semantic relation edges for the Semantic Markov model.

## Source ID

```text
conceptnet_assertions
```

## Fetch

Download into:

```text
~/.local/share/library-of-babel/sources/conceptnet/
```

Expected file:

```text
conceptnet-assertions-*.csv.gz
```

Command:

```bash
babel-source-builder source fetch conceptnet_assertions
```

Must also support:

```bash
--local-file /path/to/conceptnet-assertions.csv.gz
```

## Export Algorithm

1. stream gzipped tab-separated ConceptNet assertion rows;
2. keep English nodes only:
   - `/c/en/...`
3. normalize ConceptNet terms:
   - underscores to spaces;
   - lowercase;
   - strip POS suffix if present but preserve in metadata;
4. map terms to `lexeme`/`surface_form`;
5. create `semantic_node`;
6. insert `semantic_edge`;
7. preserve relation type:
   - `/r/RelatedTo`
   - `/r/IsA`
   - `/r/PartOf`
   - `/r/UsedFor`
   - `/r/CapableOf`
   - `/r/HasProperty`
   - etc.
8. store raw weight and dataset metadata.

## Edge Filtering

Default keep relations:

```text
RelatedTo
IsA
PartOf
HasA
UsedFor
CapableOf
AtLocation
Causes
HasProperty
Synonym
Antonym
DerivedFrom
SimilarTo
FormOf
```

Configurable allowlist:

```toml
[conceptnet]
allowed_relations = ["RelatedTo", "IsA", "UsedFor", "CapableOf", "HasProperty", "Synonym", "SimilarTo"]
language = "en"
min_weight = 0.0
```

## DuckDB Tables

```text
source_registry
source_file
lexeme
surface_form
semantic_node
semantic_edge
```

## Unit Tests

```text
tests/unit/test_conceptnet_row_parser.py
tests/unit/test_conceptnet_term_normalization.py
tests/unit/test_conceptnet_relation_filter.py
```

## Integration Tests

```text
tests/integration/test_conceptnet_fixture_export_duckdb.py
```

Full import marked:

```text
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/conceptnet.md
```

Must include:

- relation mapping;
- filtering strategy;
- semantic Markov role;
- expected size;
- limitations.

## Exit Criteria

- ConceptNet fixture exports semantic edges;
- English-only filter works;
- graph build can consume edges;
- docs and tests complete.

