# 04 - DuckDB Schema Version 1

## Objective

Define the unified DuckDB schema used by `babel-source-builder`.

The schema must support all five initial models:

1. Lexical Reduction
2. Syntactic Reduction
3. Sentence Structure
4. Grammatical Limits
5. Semantic Markov

## Schema Principles

- Raw sources are not fully duplicated unless small.
- Normalized tables preserve provenance.
- Every derived row must be traceable to one or more source rows/files.
- Runtime-facing views must be stable and simple.
- Heavy graph matrices may be external `.npz`, but their nodes/edges/provenance are represented in DuckDB.

## Core Tables

### `schema_migrations`

```sql
CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    applied_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);
```

### `source_registry`

```sql
CREATE TABLE IF NOT EXISTS source_registry (
    source_id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,
    display_name TEXT NOT NULL,
    canonical_url TEXT,
    local_path TEXT,
    license_id TEXT,
    license_text_path TEXT,
    version TEXT,
    downloaded_at TIMESTAMP,
    imported_at TIMESTAMP,
    sha256 TEXT,
    size_bytes BIGINT,
    row_count BIGINT,
    enabled BOOLEAN NOT NULL DEFAULT true,
    notes TEXT
);
```

### `source_file`

```sql
CREATE TABLE IF NOT EXISTS source_file (
    source_file_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    format TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    size_bytes BIGINT NOT NULL,
    compressed BOOLEAN NOT NULL DEFAULT false,
    imported BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

## Lexical Tables

### `lexeme`

Canonical lemma-level entry.

```sql
CREATE TABLE IF NOT EXISTS lexeme (
    lexeme_id BIGINT PRIMARY KEY,
    language TEXT NOT NULL,
    lemma TEXT NOT NULL,
    normalized_lemma TEXT NOT NULL,
    is_alpha BOOLEAN NOT NULL,
    is_phrase BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
    UNIQUE(language, normalized_lemma)
);
```

### `surface_form`

```sql
CREATE TABLE IF NOT EXISTS surface_form (
    surface_id BIGINT PRIMARY KEY,
    lexeme_id BIGINT,
    language TEXT NOT NULL,
    surface TEXT NOT NULL,
    normalized_surface TEXT NOT NULL,
    casing TEXT,
    is_runtime_allowed BOOLEAN NOT NULL DEFAULT true,
    FOREIGN KEY(lexeme_id) REFERENCES lexeme(lexeme_id),
    UNIQUE(language, normalized_surface)
);
```

### `frequency_observation`

```sql
CREATE TABLE IF NOT EXISTS frequency_observation (
    observation_id BIGINT PRIMARY KEY,
    surface_id BIGINT,
    source_id TEXT NOT NULL,
    frequency_raw DOUBLE,
    frequency_per_million DOUBLE,
    zipf_frequency DOUBLE,
    rank INTEGER,
    corpus_count BIGINT,
    metadata_json TEXT,
    FOREIGN KEY(surface_id) REFERENCES surface_form(surface_id),
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

### `runtime_vocabulary`

This is a runtime-facing materialized table.

```sql
CREATE TABLE IF NOT EXISTS runtime_vocabulary (
    runtime_rank INTEGER PRIMARY KEY,
    language TEXT NOT NULL,
    surface_id BIGINT NOT NULL,
    surface TEXT NOT NULL,
    normalized_surface TEXT NOT NULL,
    score DOUBLE NOT NULL,
    source_mix_json TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    FOREIGN KEY(surface_id) REFERENCES surface_form(surface_id)
);
```

## POS and Morphology Tables

### `pos_inventory`

```sql
CREATE TABLE IF NOT EXISTS pos_inventory (
    pos_id TEXT PRIMARY KEY,
    tagset TEXT NOT NULL,
    description TEXT
);
```

Required UPOS rows:

```text
ADJ, ADP, ADV, AUX, CCONJ, DET, INTJ, NOUN,
NUM, PART, PRON, PROPN, PUNCT, SCONJ, SYM, VERB, X
```

### `lexeme_pos`

```sql
CREATE TABLE IF NOT EXISTS lexeme_pos (
    lexeme_id BIGINT NOT NULL,
    pos_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    confidence DOUBLE NOT NULL DEFAULT 1.0,
    count BIGINT,
    metadata_json TEXT,
    PRIMARY KEY(lexeme_id, pos_id, source_id),
    FOREIGN KEY(lexeme_id) REFERENCES lexeme(lexeme_id),
    FOREIGN KEY(pos_id) REFERENCES pos_inventory(pos_id),
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

### `morphological_feature`

```sql
CREATE TABLE IF NOT EXISTS morphological_feature (
    feature_id BIGINT PRIMARY KEY,
    lexeme_id BIGINT,
    surface_id BIGINT,
    pos_id TEXT,
    features_json TEXT NOT NULL,
    source_id TEXT NOT NULL,
    FOREIGN KEY(lexeme_id) REFERENCES lexeme(lexeme_id),
    FOREIGN KEY(surface_id) REFERENCES surface_form(surface_id),
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

## Syntax and Sentence Tables

### `punctuation_inventory`

```sql
CREATE TABLE IF NOT EXISTS punctuation_inventory (
    punctuation TEXT PRIMARY KEY,
    language TEXT NOT NULL,
    class TEXT NOT NULL,
    can_start_sentence BOOLEAN NOT NULL DEFAULT false,
    can_end_sentence BOOLEAN NOT NULL DEFAULT false,
    can_repeat BOOLEAN NOT NULL DEFAULT false,
    default_weight DOUBLE NOT NULL DEFAULT 1.0
);
```

### `punctuation_transition`

```sql
CREATE TABLE IF NOT EXISTS punctuation_transition (
    previous_class TEXT NOT NULL,
    next_class TEXT NOT NULL,
    allowed BOOLEAN NOT NULL,
    weight DOUBLE NOT NULL DEFAULT 1.0,
    PRIMARY KEY(previous_class, next_class)
);
```

### `sentence_length_distribution`

```sql
CREATE TABLE IF NOT EXISTS sentence_length_distribution (
    language TEXT NOT NULL,
    profile TEXT NOT NULL,
    words_per_sentence INTEGER NOT NULL,
    probability DOUBLE NOT NULL,
    source_id TEXT,
    PRIMARY KEY(language, profile, words_per_sentence)
);
```

## Grammar Tables

### `grammar_template`

```sql
CREATE TABLE IF NOT EXISTS grammar_template (
    template_id TEXT PRIMARY KEY,
    language TEXT NOT NULL,
    source_id TEXT,
    template_json TEXT NOT NULL,
    readable_pattern TEXT NOT NULL,
    weight DOUBLE NOT NULL DEFAULT 1.0,
    enabled BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT current_timestamp
);
```

Example `template_json`:

```json
{
  "slots": [
    {"slot": 0, "upos": "DET"},
    {"slot": 1, "upos": "ADJ", "optional": true},
    {"slot": 2, "upos": "NOUN", "features": {"Number": "Sing"}},
    {"slot": 3, "upos": "VERB", "features": {"Tense": "Pres"}},
    {"slot": 4, "upos": "DET"},
    {"slot": 5, "upos": "NOUN"}
  ],
  "terminal_punctuation": [".", "?", "!"]
}
```

### `grammar_template_observation`

```sql
CREATE TABLE IF NOT EXISTS grammar_template_observation (
    observation_id BIGINT PRIMARY KEY,
    template_id TEXT NOT NULL,
    source_id TEXT NOT NULL,
    sentence_hash TEXT,
    count BIGINT NOT NULL DEFAULT 1,
    metadata_json TEXT,
    FOREIGN KEY(template_id) REFERENCES grammar_template(template_id),
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

## Corpus Tables

### `corpus_document`

```sql
CREATE TABLE IF NOT EXISTS corpus_document (
    document_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    title TEXT,
    author TEXT,
    language TEXT,
    year INTEGER,
    genre TEXT,
    license_id TEXT,
    metadata_json TEXT,
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

### `corpus_sentence`

```sql
CREATE TABLE IF NOT EXISTS corpus_sentence (
    sentence_id TEXT PRIMARY KEY,
    document_id TEXT,
    source_id TEXT NOT NULL,
    sentence_index INTEGER,
    text TEXT NOT NULL,
    token_count INTEGER,
    normalized_hash TEXT NOT NULL,
    metadata_json TEXT,
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

### `corpus_token`

```sql
CREATE TABLE IF NOT EXISTS corpus_token (
    token_id BIGINT PRIMARY KEY,
    sentence_id TEXT NOT NULL,
    token_index INTEGER NOT NULL,
    surface TEXT NOT NULL,
    normalized_surface TEXT NOT NULL,
    lemma TEXT,
    upos TEXT,
    xpos TEXT,
    features_json TEXT,
    dependency_relation TEXT,
    head_token_index INTEGER,
    source_id TEXT NOT NULL,
    FOREIGN KEY(sentence_id) REFERENCES corpus_sentence(sentence_id)
);
```

## Semantic Graph Tables

### `semantic_node`

```sql
CREATE TABLE IF NOT EXISTS semantic_node (
    node_id BIGINT PRIMARY KEY,
    language TEXT NOT NULL,
    surface_id BIGINT,
    lexeme_id BIGINT,
    node_key TEXT NOT NULL,
    upos TEXT,
    semantic_class TEXT,
    enabled BOOLEAN NOT NULL DEFAULT true,
    UNIQUE(language, node_key),
    FOREIGN KEY(surface_id) REFERENCES surface_form(surface_id),
    FOREIGN KEY(lexeme_id) REFERENCES lexeme(lexeme_id)
);
```

### `semantic_edge`

```sql
CREATE TABLE IF NOT EXISTS semantic_edge (
    edge_id BIGINT PRIMARY KEY,
    from_node_id BIGINT NOT NULL,
    to_node_id BIGINT NOT NULL,
    edge_type TEXT NOT NULL,
    source_id TEXT NOT NULL,
    raw_weight DOUBLE,
    normalized_weight DOUBLE,
    metadata_json TEXT,
    FOREIGN KEY(from_node_id) REFERENCES semantic_node(node_id),
    FOREIGN KEY(to_node_id) REFERENCES semantic_node(node_id),
    FOREIGN KEY(source_id) REFERENCES source_registry(source_id)
);
```

### `semantic_transition`

Final pruned runtime edge.

```sql
CREATE TABLE IF NOT EXISTS semantic_transition (
    from_node_id BIGINT NOT NULL,
    to_node_id BIGINT NOT NULL,
    final_weight DOUBLE NOT NULL,
    score_components_json TEXT NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT true,
    PRIMARY KEY(from_node_id, to_node_id)
);
```

## Runtime Views

### `v_runtime_vocabulary`

```sql
CREATE VIEW IF NOT EXISTS v_runtime_vocabulary AS
SELECT runtime_rank, language, surface, normalized_surface, score
FROM runtime_vocabulary
WHERE enabled = true
ORDER BY runtime_rank;
```

### `v_runtime_grammar_templates`

```sql
CREATE VIEW IF NOT EXISTS v_runtime_grammar_templates AS
SELECT template_id, language, template_json, readable_pattern, weight
FROM grammar_template
WHERE enabled = true;
```

### `v_runtime_semantic_transitions`

```sql
CREATE VIEW IF NOT EXISTS v_runtime_semantic_transitions AS
SELECT from_node_id, to_node_id, final_weight
FROM semantic_transition
WHERE enabled = true;
```

## Schema Tests

Create:

```text
tests/unit/test_schema_sql.py
tests/integration/test_duckdb_schema_creation.py
tests/integration/test_schema_migration_idempotency.py
```

Verify:

- schema creates from empty DB;
- migration is idempotent;
- all runtime views exist;
- required UPOS inventory can be inserted;
- foreign key assumptions are documented.

