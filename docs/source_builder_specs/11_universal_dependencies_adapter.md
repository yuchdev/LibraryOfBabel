# 11 - Universal Dependencies Adapter

## Objective

Import Universal Dependencies English treebanks for grammar templates, POS tags, morphology, and dependency-conditioned semantic transitions.

Initial treebanks:

```text
UD_English-EWT
UD_English-GUM
```

## Source IDs

```text
ud_english_ewt
ud_english_gum
```

## Installation

```bash
uv add conllu
```

## Fetch

```bash
babel-source-builder source fetch ud_english_ewt
babel-source-builder source fetch ud_english_gum
```

Default fetch method:

```bash
git clone --depth 1 https://github.com/UniversalDependencies/UD_English-EWT.git
git clone --depth 1 https://github.com/UniversalDependencies/UD_English-GUM.git
```

into:

```text
~/.local/share/library-of-babel/sources/universal_dependencies/
```

## Export Algorithm

1. locate `.conllu` files;
2. parse sentences with `conllu`;
3. insert `corpus_document` rows for train/dev/test files;
4. insert `corpus_sentence`;
5. insert `corpus_token` with:
   - surface;
   - lemma;
   - UPOS;
   - XPOS;
   - features;
   - dependency relation;
   - head index;
6. update `lexeme`, `surface_form`;
7. update `lexeme_pos` with observed counts;
8. extract grammar templates;
9. extract POS transition counts;
10. extract dependency edge observations.

## Grammar Template Extraction

For each sentence:

1. remove punctuation except terminal punctuation;
2. map tokens to UPOS;
3. optionally collapse repeated modifiers;
4. create readable pattern:
   - `DET ADJ? NOUN VERB DET NOUN PUNCT`
5. count occurrences;
6. discard templates below configurable count threshold;
7. store in `grammar_template`.

Config:

```toml
[ud.grammar_templates]
min_count = 5
max_slots = 24
collapse_adj_runs = true
collapse_adv_runs = true
preserve_terminal_punctuation = true
```

## Dependency Edges

Insert semantic edges for dependencies:

```text
nsubj
obj
iobj
obl
amod
advmod
compound
nmod
conj
```

Edge type examples:

```text
ud_dep:nsubj
ud_dep:obj
ud_pos_bigram
```

## DuckDB Tables

```text
source_registry
source_file
lexeme
surface_form
lexeme_pos
morphological_feature
corpus_document
corpus_sentence
corpus_token
grammar_template
grammar_template_observation
semantic_edge
```

## Unit Tests

```text
tests/unit/test_ud_conllu_parser.py
tests/unit/test_ud_template_extraction.py
tests/unit/test_ud_dependency_edge_extraction.py
tests/unit/test_ud_pos_mapping.py
```

## Integration Tests

```text
tests/integration/test_ud_fixture_export_duckdb.py
tests/integration/test_ud_ewt_export_duckdb.py
```

Network/full-data tests marked:

```text
@pytest.mark.network
@pytest.mark.large_data
```

## Documentation

```text
docs/sources/universal_dependencies.md
```

Must include:

- required treebanks;
- license notes per treebank;
- grammar template algorithm;
- dependency edge algorithm;
- examples of extracted templates.

## Exit Criteria

- UD data exported to DuckDB;
- grammar templates generated;
- dependency edges generated;
- POS observations generated;
- docs and tests complete.

