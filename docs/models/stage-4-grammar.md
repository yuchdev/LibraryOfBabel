# Stage 4 - Categorical Grammar Constraint

1. Canonical article name: Categorical Grammar Constraint  
2. App mode ID: `grammar-constrained`  
3. Formula: `(D·A·N·V·D·N·P)^R`  
4. Data used: `wordnet` POS files if available, otherwise deterministic built-in POS fallback  
5. Class/path: `GrammarConstrainedGenerator` in `src/babel/generators/grammar_constrained.py`  
6. Determinism: template-cycled deterministic index by POS namespace  
7. Limitations: fallback POS lists are lightweight demo data  
8. CLI: `uv run library-of-babel metrics --mode grammar-constrained`  
9. API:
   ```python
   from babel.generators.grammar_constrained import GrammarConstrainedGenerator
   ```
10. Tests: `tests/generators/test_grammar_constrained.py`, `tests/vocabulary/test_vocab_loading.py`

