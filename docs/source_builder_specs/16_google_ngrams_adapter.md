# 16 — Google Books Ngram Adapter

## Objective

Import selected n-gram counts for frequency priors and Markov transition edges.

## Source IDs

```text
google_books_1grams
google_books_2grams
google_books_3grams
```

Higher n-grams are optional.

## Warning

Google Ngram is large.

The adapter must support selective streaming and filtering. It must not require downloading the entire dataset for the application.

## Fetch Strategy

Supported modes:

```text
index-only
selected-files
local-file
```

Commands:

```bash
babel-source-builder source fetch google_ngrams --index-only
babel-source-builder source fetch google_ngrams --ngram 1 --letters a,b,c
babel-source-builder source fetch google_ngrams --local-file /path/to/file.gz
```

## Export Algorithm

### 1-Grams

1. stream rows;
2. normalize token;
3. filter language/valid token;
4. aggregate counts by token over years;
5. insert/update `frequency_observation`.

### 2-Grams

1. stream rows;
2. split ngram;
3. normalize both terms;
4. keep only if both terms are in runtime vocabulary candidate set;
5. aggregate counts;
6. insert `semantic_edge` with edge type `corpus_bigram:google_books`.

### 3-Grams

Optional:

1. use for grammar/context diagnostics;
2. can generate second-order Markov edges;
3. store as compressed derived table only if enabled.

## DuckDB Tables

```text
source_registry
source_file
frequency_observation
semantic_node
semantic_edge
```

Optional:

```sql
CREATE TABLE IF NOT EXISTS ngram_observation (
    ngram_id BIGINT PRIMARY KEY,
    source_id TEXT NOT NULL,
    n INTEGER NOT NULL,
    ngram_text TEXT NOT NULL,
    normalized_json TEXT NOT NULL,
    match_count BIGINT,
    volume_count BIGINT,
    year_min INTEGER,
    year_max INTEGER
);
```

## Config

```toml
[google_ngrams]
language = "eng"
max_ngram = 2
min_total_count = 100
filter_to_runtime_vocabulary = true
```

## Unit Tests

```text
tests/unit/test_google_ngram_row_parser.py
tests/unit/test_google_ngram_filtering.py
tests/unit/test_google_ngram_aggregation.py
```

## Integration Tests

```text
tests/integration/test_google_ngram_fixture_export_duckdb.py
```

Network/large tests:

```text
@pytest.mark.network
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/google_ngrams.md
```

Must include:

- huge-size warning;
- selective fetch examples;
- supported n values;
- exact export algorithm;
- how bigram edges are scored.

## Exit Criteria

- fixture ngram file exports frequency and bigram edges;
- full dataset not required for normal CI;
- docs and tests complete.

