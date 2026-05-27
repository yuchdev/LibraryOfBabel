# Stage 5 - Markovian Semantic Adjacency Constraint

1. Canonical article name: Markovian Semantic Adjacency Constraint  
2. App mode ID: `semantic-constrained`  
3. Formula: `≈ λ_max^N` (lightweight local graph approximation)  
4. Data used: `words.txt` + shared punctuation `. ? , !`  
5. Class/path: `SemanticConstrainedGenerator` in `src/babel/generators/semantic_constrained.py`  
6. Determinism: explicit adjacency map + deterministic transition selection  
7. Limitations: not full WordNet-scale semantic relation graph; lightweight local approximation  
8. CLI: `uv run library-of-babel page --mode semantic-constrained --seed test --page 0`  
9. API:
   ```python
   from babel.generators.semantic_constrained import SemanticConstrainedGenerator
   ```
10. Tests: `tests/generators/test_semantic_constrained.py`

