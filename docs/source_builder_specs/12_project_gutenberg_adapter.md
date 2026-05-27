# 12 - Project Gutenberg / SPGC Adapter

## Objective

Import a literary corpus for sentence distributions, word frequencies, and Markov transition counts.

Preferred source:

```text
Standardized Project Gutenberg Corpus / SPGC
```

Legacy/light source:

```text
NLTK Gutenberg
```

## Source ID

```text
project_gutenberg_spgc
```

## Important Access Rule

Do not aggressively scrape Project Gutenberg web pages.

The adapter must use one of:

- SPGC prepared/reproducible pipeline;
- official mirror/offline data;
- user-provided local corpus directory;
- Kaggle fallback dataset when explicitly configured.

## Fetch

Default command should not download all Gutenberg automatically unless user passes:

```bash
--large-data
```

Example:

```bash
babel-source-builder source fetch project_gutenberg_spgc --large-data
```

## Export Algorithm

1. discover text files in configured SPGC/local corpus;
2. collect metadata if available:
   - title;
   - author;
   - language;
   - year;
   - genre;
   - license;
3. clean boilerplate if source is not already cleaned;
4. sentence-split;
5. tokenize;
6. insert documents/sentences/tokens;
7. compute:
   - sentence length distribution;
   - terminal punctuation distribution;
   - token frequencies;
   - bigram/trigram counts;
   - optional literary-style grammar templates.

## DuckDB Tables

```text
source_registry
source_file
corpus_document
corpus_sentence
corpus_token
frequency_observation
sentence_length_distribution
semantic_edge
grammar_template_observation
```

## Tests

Unit:

```text
tests/unit/test_gutenberg_text_cleaning.py
tests/unit/test_gutenberg_sentence_split.py
tests/unit/test_gutenberg_metadata_mapping.py
```

Integration:

```text
tests/integration/test_gutenberg_fixture_export_duckdb.py
```

Full corpus test:

```text
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/project_gutenberg.md
```

Must include:

- safe/legal access methods;
- how to use local SPGC data;
- what is imported;
- boilerplate limitations;
- expected disk usage.

## Exit Criteria

- local fixture corpus exports;
- sentence distributions exported;
- bigram/trigram edges exported;
- docs and tests complete.

