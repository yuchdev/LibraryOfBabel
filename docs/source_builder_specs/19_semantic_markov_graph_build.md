# 19 - Semantic Markov Graph Build

## Objective

Build the final pruned transition graph used by the Semantic Markov generation model.

## Core Idea

A good Semantic Markov graph must combine several weak signals:

- observed word adjacency;
- POS compatibility;
- dependency compatibility;
- semantic relations;
- embedding similarity;
- frequency prior;
- grammar template state.

No single source is enough.

## Node Definition

Preferred node:

```text
node = normalized_surface + optional UPOS + optional semantic_class
```

Minimal node:

```text
node = normalized_surface
```

Config:

```toml
[semantic_markov]
node_mode = "surface_upos"
```

Allowed values:

```text
surface
lemma
surface_upos
lemma_upos
```

## Edge Sources

```text
corpus_bigram:google_books
corpus_bigram:gutenberg
corpus_bigram:brown
ud_dependency:nsubj
ud_dependency:obj
conceptnet:RelatedTo
conceptnet:IsA
wordnet:hypernym
wordnet:synonym
embedding_similarity:glove
embedding_similarity:fasttext
embedding_similarity:numberbatch
```

## Composite Scoring

For edge `a -> b`:

```text
score =
    alpha * corpus_bigram_score
  + beta  * pos_transition_score
  + gamma * dependency_score
  + delta * conceptnet_score
  + eps   * wordnet_score
  + zeta  * embedding_similarity_score
  + eta   * frequency_prior
```

Default weights:

```toml
[semantic_markov.weights]
corpus_bigram = 3.0
pos_transition = 2.0
dependency = 2.0
conceptnet = 1.5
wordnet = 1.2
embedding_similarity = 1.0
frequency_prior = 0.5
```

## Build Algorithm

1. load runtime vocabulary;
2. create semantic nodes;
3. import all candidate edges from `semantic_edge`;
4. normalize source-specific weights;
5. compute composite score;
6. filter invalid POS transitions;
7. prune:
   - top K outgoing edges per node;
   - min score threshold;
   - remove self loops unless allowed;
8. normalize outgoing weights to probabilities;
9. write `semantic_transition`;
10. export CSR matrix:
    - row = from node;
    - column = to node;
    - value = normalized weight;
11. export `node_index.parquet`;
12. compute graph metrics:
    - node count;
    - edge count;
    - isolated nodes;
    - average out-degree;
    - dominant eigenvalue estimate;
    - strongly connected component summary.

## Pruning Config

```toml
[semantic_markov.pruning]
max_out_edges = 64
min_score = 0.05
allow_self_loops = false
require_pos_compatibility = true
fallback_edges_for_isolated_nodes = true
```

## Handling Isolated Nodes

If a node has no outgoing edges:

1. try embedding nearest neighbors;
2. try same POS high-frequency words;
3. fallback to common determiners or sentence starters;
4. mark fallback in `score_components_json`.

## Determinism

The graph build must be deterministic:

- stable sorting;
- explicit tie-breakers;
- fixed random seed if sampling is unavoidable;
- no unordered set iteration in final ranking.

## Tests

Unit:

```text
tests/unit/test_semantic_score_combination.py
tests/unit/test_semantic_pruning.py
tests/unit/test_semantic_isolated_node_fallback.py
tests/unit/test_semantic_csr_export.py
```

Integration:

```text
tests/integration/test_semantic_graph_build_from_fixture_db.py
tests/integration/test_semantic_graph_deterministic_rebuild.py
```

## QA Metrics

Graph build must produce:

```text
derived/semantic_markov/graph_stats.json
```

Required fields:

```json
{
  "nodes": 0,
  "edges": 0,
  "average_out_degree": 0.0,
  "isolated_nodes": 0,
  "fallback_edges": 0,
  "dominant_eigenvalue_estimate": null
}
```

## Exit Criteria

- graph builds from fixture DB;
- CSR output loads in `babel`;
- deterministic rebuild produces identical checksums;
- graph stats exported;
- tests and docs complete.

