# 18 — Export Algorithms by Model

## Objective

Define how DuckDB data is transformed into runtime artifacts for the first five models.

## Model 1 — Lexical Reduction

### Inputs

```text
lexeme
surface_form
frequency_observation
legacy_vocabulary
wordfreq
WordNet
Kaggle frequency fallbacks
Google 1-grams
```

### Output

```text
runtime_vocabulary
```

### Algorithm

1. collect candidate surface forms;
2. normalize and deduplicate;
3. calculate source score:
   - frequency rank;
   - wordfreq score;
   - legacy priority;
   - WordNet/Wiktionary validation;
4. remove disabled tokens;
5. sort by final score;
6. assign `runtime_rank`;
7. export table and optional JSONL.

## Model 2 — Syntactic Reduction

### Inputs

```text
punctuation_inventory
punctuation_transition
runtime_vocabulary
corpus punctuation stats
```

### Output

```text
punctuation_inventory
punctuation_transition
```

### Algorithm

1. create default punctuation inventory;
2. derive punctuation frequencies from corpora if available;
3. enforce no adjacent punctuation rule;
4. export punctuation class config.

## Model 3 — Sentence Structure

### Inputs

```text
corpus_sentence
corpus_token
punctuation stats
```

### Output

```text
sentence_length_distribution
terminal punctuation weights
```

### Algorithm

1. compute token count per sentence;
2. remove outliers based on config;
3. build empirical distribution;
4. add strict profile:
   - 15 words per sentence;
5. add literary profile if Gutenberg is available;
6. add dialogue profile if OpenSubtitles/Kaggle subtitles are available.

## Model 4 — Grammatical Limits

### Inputs

```text
lexeme_pos
morphological_feature
grammar_template
UD treebanks
Wiktionary
WordNet
```

### Output

```text
grammar_template
runtime grammar views
POS-filtered vocabulary pools
```

### Algorithm

1. build POS pools by UPOS;
2. resolve ambiguous POS using source confidence and corpus counts;
3. extract templates from UD;
4. filter templates by count and max length;
5. ensure closed-class words are available:
   - DET
   - ADP
   - AUX
   - PRON
   - CCONJ
   - SCONJ
   - PART
6. export runtime templates.

## Model 5 — Semantic Markov

### Inputs

```text
semantic_node
semantic_edge
runtime_vocabulary
lexeme_pos
grammar_template
embeddings
ConceptNet
WordNet
UD dependencies
Google/Gutenberg bigrams
```

### Output

```text
semantic_transition
graph/semantic_graph_csr.npz
graph/node_index.parquet
graph/edge_weights.parquet
```

### Algorithm

See `19_semantic_markov_graph_build.md`.

## Tests

Create:

```text
tests/unit/test_export_lexical.py
tests/unit/test_export_syntax.py
tests/unit/test_export_sentence.py
tests/unit/test_export_grammar.py
tests/unit/test_export_semantic_markov.py
tests/integration/test_export_all_models_from_fixture_db.py
```

## Exit Criteria

- each model has a deterministic export;
- fixture DB can produce all runtime artifacts;
- exported artifacts validate against source pack contract.

