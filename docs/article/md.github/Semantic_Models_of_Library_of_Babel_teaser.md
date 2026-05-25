# From Borges to Meaning: Progressive Reduction of the Library of Babel

## Table of Contents

- [Abstract](#abstract)
- [1. Original Borges Library](#1-original-borges-library)
- [2. Word-Based Library](#2-word-based-library)
  - [Motivation](#motivation)
  - [Python Generator](#python-generator)
- [3. Punctuation-Constrained Library](#3-punctuation-constrained-library)
  - [Constraint](#constraint)
  - [Combinatorics](#combinatorics)
  - [Python Implementation](#python-implementation)
- [4. Sentence-Structured Library](#4-sentence-structured-library)
  - [Constraint](#constraint-1)
  - [Python Generator](#python-generator-1)
- [5. Grammar-Constrained Library](#5-grammar-constrained-library)
  - [Constraint](#constraint-2)
  - [Combinatorics](#combinatorics-1)
  - [Python Implementation](#python-implementation-1)
- [6. Semantic-Constrained Library](#6-semantic-constrained-library)
  - [Constraint](#constraint-3)
  - [Markov Formulation](#markov-formulation)
  - [Python Implementation](#python-implementation-2)
- [7. Topic-Coherent Library](#7-topic-coherent-library)
  - [Constraint](#constraint-4)
  - [Information-Theoretic Interpretation](#information-theoretic-interpretation)
- [8. Final Observation](#8-final-observation)

---

## Abstract

This article investigates a sequence of mathematical transformations of *The Library of Babel*, originally proposed by Jorge Luis Borges. Starting from the classical combinatoric construction containing every possible sequence of characters, we progressively constrain the Library so that:

1. the number of possible books decreases;
2. the average semantic density increases;
3. random pages become increasingly human-readable.

At each stage we introduce:

- a mathematical model;
- combinatoric analysis;
- asymptotic reduction;
- Python algorithms capable of generating pages on demand from compact seeds.

The experiment reveals a transition from pure entropy toward structured language and eventually toward semantic manifolds approximating meaningful literature.

---

## 1. Original Borges Library

Borges defines books with:

- 410 pages;
- 40 lines per page;
- 80 characters per line;
- an alphabet of 25 symbols.

Total character positions:

```math
C = 410 \times 40 \times 80
```

```math
410 \times 40 \times 80 = 1{,}312{,}000
```

Total number of books:

```math
25^{1{,}312{,}000}
```

Approximation:

```math
25^{1{,}312{,}000}
\approx
1.95 \times 10^{1{,}834{,}097}
```

This construction maximizes entropy but minimizes meaning.

Almost every book is unreadable noise.

---

## 2. Word-Based Library

### Motivation

Human language is not constructed from arbitrary character sequences.

Replacing characters with words immediately injects semantic structure.

Assume:

- vocabulary size:

  ```math
  W = 100{,}000
  ```

- punctuation symbols:

  ```math
  P = 6
  ```

- average token width is approximately 6 characters.

Approximate token slots:

```math
N \approx \frac{1{,}312{,}000}{6}
```

```math
N \approx \frac{1{,}312{,}000}{6} \approx 218{,}667
```

Total books:

```math
(100{,}006)^{218{,}667}
```

Approximation:

```math
(100{,}006)^{218{,}667}
\approx
10^{1{,}093{,}340}
```

The Library shrinks enormously while readability increases dramatically.

### Python Generator

```python
import hashlib

VOCABULARY = ["the", "house", "river", "memory", "darkness"]

def token_at(seed: str, position: int):
    data = f"{seed}:{position}".encode("utf-8")
    digest = hashlib.sha256(data).digest()
    value = int.from_bytes(digest[:8], "big")
    return VOCABULARY[value % len(VOCABULARY)]

def generate_page(seed, page, tokens_per_page=300):
    start = page * tokens_per_page
    return [
        token_at(seed, i)
        for i in range(start, start + tokens_per_page)
    ]
```

The complete book never needs to exist in memory.

---

## 3. Punctuation-Constrained Library

### Constraint

No two punctuation marks may appear consecutively.

This removes sequences like:

```text
word . ? , !
```

which are structurally invalid.

### Combinatorics

If exactly $k$ punctuation marks appear, the number of valid placements without adjacency is:

```math
\binom{N-k+1}{k}
```

Therefore, the total Library size is:

```math
\sum_{k=0}^{\lfloor(N+1)/2\rfloor}
\binom{N-k+1}{k}
P^k
W^{N-k}
```

This slightly reduces entropy while improving grammatical plausibility.

### Python Implementation

```python
def valid_sequence(tokens):
    punct = {".", ",", ";", ":", "?", "!"}

    for i in range(len(tokens) - 1):
        if tokens[i] in punct and tokens[i + 1] in punct:
            return False

    return True
```

---

## 4. Sentence-Structured Library

### Constraint

Every sentence must contain:

- exactly 15 words;
- followed by one punctuation mark.

Pattern:

```text
W W W W W W W W W W W W W W W P
```

Sentence count:

```math
S = \left\lfloor \frac{N}{16} \right\rfloor
```

Total Library:

```math
W^{15S} P^S
```

Approximation:

```math
W^{15S} P^S
\approx
10^{1{,}035{,}639}
```

The Library loses vast amounts of entropy while gaining strong textual regularity.

Random pages now resemble primitive prose.

### Python Generator

```python
WORDS_PER_SENTENCE = 15

PUNCT = [".", "?", "!"]

def sentence(seed, index):
    words = [
        token_at(seed, index * 16 + i)
        for i in range(WORDS_PER_SENTENCE)
    ]

    punct = PUNCT[
        hash(f"{seed}:{index}") % len(PUNCT)
    ]

    return " ".join(words) + punct
```

---

## 5. Grammar-Constrained Library

### Constraint

Sentences must satisfy grammatical templates.

Example:

```text
DET ADJ NOUN VERB DET NOUN .
```

Define vocabulary partitions:

- nouns;
- verbs;
- adjectives;
- adverbs;
- determiners;
- pronouns;
- prepositions.

### Combinatorics

If $D$, $A$, $N$, and $V$ represent category counts, then one sentence template produces:

```math
D \cdot A \cdot N \cdot V \cdot D \cdot N \cdot P
```

possible sentences.

A book with $S$ such sentences gives:

```math
(DANVDNP)^S
```

This reduction is enormous.

However, readability increases dramatically.

Random pages now resemble machine-generated language.

### Python Implementation

```python
GRAMMAR = [
    ("DET", ["the", "a"]),
    ("ADJ", ["dark", "ancient"]),
    ("NOUN", ["river", "library", "mirror"]),
    ("VERB", ["contains", "reflects"]),
    ("DET", ["the", "a"]),
    ("NOUN", ["truth", "memory"]),
]

def grammar_sentence(seed, sentence_id):
    words = []

    for i, (_, vocab) in enumerate(GRAMMAR):
        token = token_at(seed, sentence_id * 100 + i)
        words.append(vocab[hash(token) % len(vocab)])

    return " ".join(words) + "."
```

---

## 6. Semantic-Constrained Library

### Constraint

Not all grammatically valid sentences are meaningful.

Introduce semantic neighborhoods.

Example:

```text
river ↔ water ↔ flow ↔ current
library ↔ books ↔ shelves ↔ archive
```

Words may only follow semantically compatible words.

This transforms the Library from a combinatoric explosion into a constrained semantic graph.

### Markov Formulation

Let:

```math
T_{ij}
```

be the transition probability from token $i$ to token $j$.

Then valid books are paths through the semantic graph.

Approximate sequence count:

```math
\lambda_{\max}^N
```

where:

```math
\lambda_{\max}
```

is the dominant eigenvalue of the transition matrix.

This is a profound reduction.

Meaning emerges from spectral constraints.

### Python Implementation

```python
import random

GRAPH = {
    "river": ["water", "flow", "stone"],
    "water": ["current", "river"],
    "library": ["books", "archive"],
}

def semantic_walk(seed, start, length):
    random.seed(seed)

    word = start
    result = [word]

    for _ in range(length - 1):
        next_words = GRAPH.get(word, [word])
        word = random.choice(next_words)
        result.append(word)

    return result
```

---

## 7. Topic-Coherent Library

### Constraint

Entire books must remain inside a thematic manifold.

Examples:

- cosmology;
- grief;
- mathematics;
- theology;
- medieval warfare.

This introduces long-range coherence.

Now the Library approximates actual literature.

### Information-Theoretic Interpretation

The original Borges Library maximizes entropy:

```math
H_{\max}
```

Every subsequent constraint reduces entropy:

```math
H_1 > H_2 > H_3 > H_4
```

while increasing mutual information:

```math
I(\text{text}; \text{meaning})
```

The experiment demonstrates that human-readable language occupies an infinitesimally thin manifold inside the full combinatoric space of possible books.

---

## 8. Final Observation

The original Library is not terrifying because it contains all books.

It is terrifying because meaningful books are drowned inside an ocean of entropy.

Each constraint introduced in this article:

- decreases combinatoric volume;
- increases semantic density;
- moves the Library closer to the tiny structured region inhabited by human thought.

The true Library of meaning is not infinite.

It is an extraordinarily compressed island hidden inside Borges' cosmic desert of symbols.
