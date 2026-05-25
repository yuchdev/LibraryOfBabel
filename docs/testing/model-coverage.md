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
