# Stage 2 - Syntactic Reduction (Punctuation Constraint)

1. Canonical article name: Syntactic Reduction Model (Punctuation Constraint)  
2. App mode ID: `punctuation-constrained`  
3. Formula: `Σ binom(N-k+1,k) P^k W^(N-k)`  
4. Data used: `words.txt` + shared punctuation `. ? , !`  
5. Class/path: `PunctuationConstrainedGenerator` in `src/babel/generators/punctuation_constrained.py`  
6. Determinism: constrained deterministic token chooser with page-boundary state replay  
7. Limitations: pre-page replay is linear in absolute position  
8. CLI: `uv run library-of-babel metrics --mode punctuation-constrained`  
9. API:
   ```python
   from babel.generators.punctuation_constrained import PunctuationConstrainedGenerator
   ```
10. Tests: `tests/test_punctuation_constrained.py`, `tests/mathlib/test_combinatorics.py`

