# Model and Vocabulary Coverage

Run targeted checks for model/vocabulary/math modules:

```bash
uv run pytest --cov=src/babel/generators --cov=src/babel/vocabulary --cov=src/babel/mathlib --cov-report=term-missing
```

Primary model tests:

- `tests/generators/test_constants.py`
- `tests/generators/test_model_metadata.py`
- `tests/generators/test_borges_library.py`
- `tests/generators/test_grammar_constrained.py`
- `tests/generators/test_semantic_constrained.py`
- `tests/generators/test_topic_coherent.py`
- existing stage tests under `tests/test_*.py`

Vocabulary and combinatorics tests created for this alignment work:

- `tests/vocabulary/test_sources.py`
  - verifies source IDs, expected WordNet POS files, download URL presence, serialization.
- `tests/vocabulary/test_vocab_loading.py`
  - verifies WordNet-style POS loader behavior with fixture files.
- `tests/mathlib/test_combinatorics.py`
  - validates Stage 2 combinatorics formula with brute-force small-N enumeration.

CLI model metadata smoke test:

- `tests/cli/test_model_modes.py`
  - verifies article-stage metadata appears in `library-of-babel info` output.
