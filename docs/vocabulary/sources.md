# Vocabulary Sources

## Registry

Source registry class: `VocabularySource` in `src/babel/vocabulary/sources.py`.

- Purpose: defines known source IDs, expected files, install metadata, and stage suitability.
- Expected files:
  - `scowl`: `words.txt`, `metadata.json`
  - `wordnet`: `words.txt`, `nouns.txt`, `verbs.txt`, `adjectives.txt`, `adverbs.txt`, `metadata.json`
  - `wordfreq_25k`: `english_top_25000.json`, `words.txt`, `metadata.json`
  - `subtlex_us`: `words.txt`, `frequencies.csv`, `metadata.json`
- Example:
  ```python
  from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES
  source = KNOWN_VOCABULARY_SOURCES["wordnet"]
  ```
- Failure modes:
  - unknown source IDs raise `ValueError` in installer APIs
  - non-downloadable sources raise `NotImplementedError` for auto-install
- Article stage relation:
  - Stage 1–3: lexical vocab sources
  - Stage 4–5: POS/semantic-friendly WordNet source
  - Stage 6: lightweight topic demo vocab

## Loader and Discovery APIs

- `load_words(path)` (`src/babel/vocabulary/loader.py`): deterministic local word loading.
- `load_pos_vocab(base_dir)` (`src/babel/vocabulary/loader.py`): optional POS file loading for Stage 4.
- `resolve_vocabulary_path(...)` (`src/babel/vocabulary/discovery.py`): local-first vocabulary path resolution.
- `install_source(...)` / `install_all_sources(...)` (`src/babel/vocabulary/installer.py`): explicit setup command helpers.
