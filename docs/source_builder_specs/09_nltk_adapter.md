# 09 — NLTK Adapter

## Objective

Use NLTK resources for lexical, corpus, and sentence statistics.

Sources:

```text
wordnet
omw-1.4
brown
gutenberg
punkt / punkt_tab
```

## Source IDs

```text
nltk_wordnet
nltk_brown
nltk_gutenberg
```

These may share one adapter implementation but must register separate source IDs.

## Installation

```bash
uv add nltk
```

## Download

```bash
babel-source-builder source fetch nltk
```

Must internally run NLTK downloader into:

```text
~/.local/share/library-of-babel/sources/nltk_data/
```

Do not pollute global NLTK directories unless explicitly requested.

## Export Algorithm

### WordNet

1. iterate synsets;
2. extract lemma names;
3. map WordNet POS to UPOS:
   - `n` -> `NOUN`
   - `v` -> `VERB`
   - `a`, `s` -> `ADJ`
   - `r` -> `ADV`
4. insert lexemes and surface forms;
5. insert `lexeme_pos`;
6. create semantic edges:
   - synonym;
   - hypernym;
   - hyponym;
   - meronym if available;
   - antonym if available.

### Brown

1. iterate categories/files/sentences;
2. tokenize;
3. store corpus documents/sentences/tokens;
4. compute sentence length distribution;
5. compute token bigram counts;
6. optionally import tagged POS if available.

### Gutenberg

1. iterate NLTK Gutenberg texts;
2. split sentences;
3. store documents/sentences;
4. compute literary sentence length distribution;
5. compute token frequencies and bigrams.

## DuckDB Tables

Populated:

```text
source_registry
lexeme
surface_form
lexeme_pos
semantic_edge
corpus_document
corpus_sentence
corpus_token
sentence_length_distribution
semantic_edge
```

## Tests

Unit:

```text
tests/unit/test_nltk_adapter_wordnet_mapping.py
tests/unit/test_nltk_adapter_sentence_stats.py
```

Integration:

```text
tests/integration/test_nltk_download_to_data_root.py
tests/integration/test_nltk_wordnet_export_duckdb.py
tests/integration/test_nltk_brown_gutenberg_export_duckdb.py
```

## Documentation

```text
docs/sources/nltk.md
```

Must include:

- how NLTK data directory is controlled;
- which corpora are required;
- how to redownload;
- disk usage;
- limitations of NLTK WordNet and small corpora.

## Exit Criteria

- NLTK data is downloaded into project data root;
- WordNet rows exported;
- Brown/Gutenberg sentence statistics exported;
- semantic edges from WordNet exported;
- docs and tests complete.

