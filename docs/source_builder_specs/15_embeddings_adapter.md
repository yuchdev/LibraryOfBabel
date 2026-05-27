# 15 - Embeddings Adapter: GloVe, fastText, Numberbatch

## Objective

Import vector embeddings and nearest-neighbor semantic similarity edges.

Supported embeddings:

```text
glove
fasttext
conceptnet_numberbatch
```

## Source IDs

```text
glove_6b
fasttext_crawl_300d
conceptnet_numberbatch
```

## Storage Strategy

Do not store full high-dimensional vectors directly in normal relational tables unless small.

Recommended:

```text
~/.local/share/library-of-babel/build/embeddings/
  glove_6b.filtered.npy
  glove_6b.index.parquet
  fasttext.filtered.npy
  fasttext.index.parquet
  numberbatch.filtered.npy
  numberbatch.index.parquet
```

DuckDB stores:

- source metadata;
- vector index metadata;
- nearest-neighbor semantic edges.

## Export Algorithm

1. read runtime vocabulary candidate list;
2. stream embedding file line by line;
3. keep only words present in candidate vocabulary;
4. write compact matrix `.npy`;
5. write vector index table;
6. compute nearest neighbors in batches;
7. insert similarity edges into `semantic_edge`.

## Similarity Edge Type

```text
embedding_similarity:glove
embedding_similarity:fasttext
embedding_similarity:numberbatch
```

## Config

```toml
[embeddings]
max_vocab = 100000
dimensions = 300
nearest_neighbors = 25
min_cosine = 0.45
batch_size = 4096
```

## DuckDB Tables

```text
source_registry
source_file
semantic_node
semantic_edge
```

Optional metadata table:

```sql
CREATE TABLE IF NOT EXISTS embedding_index (
    embedding_id TEXT NOT NULL,
    node_id BIGINT NOT NULL,
    row_index INTEGER NOT NULL,
    vector_file TEXT NOT NULL,
    PRIMARY KEY(embedding_id, node_id)
);
```

## Unit Tests

```text
tests/unit/test_embedding_text_parser.py
tests/unit/test_embedding_filtering.py
tests/unit/test_embedding_similarity.py
```

## Integration Tests

```text
tests/integration/test_embedding_fixture_export_duckdb.py
```

Full embedding tests marked:

```text
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/embeddings.md
```

Must include:

- supported formats;
- why vectors are filtered;
- memory requirements;
- nearest-neighbor algorithm;
- limitations of distributional similarity.

## Exit Criteria

- tiny embedding fixture exports similarity edges;
- filtered vector matrix generated;
- graph build can consume embedding edges;
- docs and tests complete.

