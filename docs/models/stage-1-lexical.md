# Stage 1 — Lexical Reduction Model

1. Canonical article name: Lexical Reduction Model  
2. App mode ID: `word-based`  
3. Formula: `(W+P)^N`, with `N=218,667`, `P=4`  
4. Data used: `words.txt` + shared punctuation `. ? , !`  
5. Class/path: `WordBasedGenerator` in `src/babel/generators/word_based.py`  
6. Determinism: direct deterministic index into `words + punctuation`  
7. Limitations: no semantic/grammar constraints  
8. CLI: `uv run library-of-babel page --mode word-based --seed test --page 0`  
9. API:
   ```python
   from babel.generators.word_based import WordBasedGenerator
   ```
10. Tests: `tests/test_word_based.py`

