# Stage 3 — Sentence-Structured Uniformity Constraint

1. Canonical article name: Sentence-Structured Uniformity Constraint  
2. App mode ID: `sentence-structured`  
3. Formula: `W^(15S) P^S`, `S=floor(N/16)`  
4. Data used: `words.txt` + shared punctuation `. ? , !`  
5. Class/path: `SentenceStructuredGenerator` in `src/babel/generators/sentence_structured.py`  
6. Determinism: absolute-position modulo 16 cycle (`15 words + 1 punctuation`)  
7. Limitations: fixed block length only  
8. CLI: `uv run library-of-babel page --mode sentence-structured --seed test --page 0`  
9. API:
   ```python
   from babel.generators.sentence_structured import SentenceStructuredGenerator
   ```
10. Tests: `tests/test_sentence_structured.py`

