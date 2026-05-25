# Stage 6 — Topic-Coherent Manifold Approximation

1. Canonical article name: Topic-Coherent Manifold / Topic-Constrained Vocabulary Model  
2. App mode ID: `topic-coherent`  
3. Formula: `Σ_topic (|V_topic|+P)^N`  
4. Data used: explicit local topic wordsets + punctuation `. ? , !`  
5. Class/path: `TopicCoherentGenerator` in `src/babel/generators/topic_coherent.py`  
6. Determinism: seed-determined topic selection and deterministic token indexing  
7. Limitations: lightweight approximation, not embedding-manifold inference  
8. CLI: `uv run library-of-babel metrics --mode topic-coherent`  
9. API:
   ```python
   from babel.generators.topic_coherent import TopicCoherentGenerator
   ```
10. Tests: `tests/generators/test_topic_coherent.py`
