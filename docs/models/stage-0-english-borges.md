# Stage 0 — English-Language Borges Baseline

1. Canonical article name: English-Language Borges Baseline  
2. App mode ID: `borges-library`  
3. Formula: `31^1,312,000`  
4. Data used: no vocabulary files; fixed alphabet `abcdefghijklmnopqrstuvwxyz .?,!`  
5. Class/path: `BorgesLibraryGenerator` in `src/babel/generators/borges_library.py`  
6. Determinism: `deterministic_uint64`-derived index by `(seed, mode, absolute_position)`  
7. Limitations: preview page rendering only; full-book generation is not supported  
8. CLI: `uv run library-of-babel metrics --mode borges-library`  
9. API:
   ```python
   from babel.generators.borges_library import BorgesLibraryGenerator
   ```
10. Tests: `tests/generators/test_borges_library.py`

