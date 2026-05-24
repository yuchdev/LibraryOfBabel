# From Borges to Meaning: Progressive Reduction of the Library of Babel

## Abstract

This article investigates a sequence of mathematical transformations of The Library of Babel originally proposed by Jorge Luis Borges. Starting from the classical combinatoric construction containing every possible sequence of characters, we progressively constrain the Library so that:

1. the number of possible books decreases,
2. the average semantic density increases,
3. random pages become increasingly human-readable.

At each stage we introduce:

* a mathematical model,
* combinatoric analysis,
* asymptotic reduction,
* Python algorithms that are capable of generating pages on demand from compact seeds.

The experiment reveals a transition from pure entropy toward structured language and eventually toward semantic manifolds approximating meaningful literature.

---

# 1. Original Borges Library

Borges defines books with:

* 410 pages,
* 40 lines/page,
* 80 characters/line,
* alphabet of 25 symbols.

Total character positions:

[
C = 410 \times 40 \times 80
]

410\times40\times80=1{,}312{,}000

Total number of books:

25^{1{,}312{,}000}

Approximation:

[
25^{1{,}312{,}000}
\approx
1.95 \times 10^{1{,}834{,}097}
]

This construction maximizes entropy but minimizes meaning.

Almost every book is unreadable noise.

---

# 2. Word-Based Library

## Motivation

Human language is not constructed from arbitrary character sequences.

Replacing characters with words immediately injects semantic structure.

Assume:

* vocabulary size:
  [
  W = 100{,}000
  ]
* punctuation symbols:
  [
  P = 6
  ]
* average token width ≈ 6 characters.

Approximate token slots:

[
N \approx \frac{1{,}312{,}000}{6}
]

N\approx\frac{1{,}312{,}000}{6}\approx218{,}667

Total books:

(100{,}006)^{218{,}667}

Approximation:

[
\approx 10^{1{,}093{,}340}
]

The Library shrinks enormously while readability increases dramatically.

---

## Python generator

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

# 3. Punctuation-Constrained Library

## Constraint

No two punctuation marks may appear consecutively.

This removes sequences like:

```text
word . ? , !
```

which are structurally invalid.

---

## Combinatorics

If exactly (k) punctuation marks appear:

[
\binom{N-k+1}{k}
]

ways exist to place them without adjacency.

Total Library:

\sum_{k=0}^{\lfloor(N+1)/2\rfloor}\binom{N-k+1}{k}P^kW^{N-k}

This slightly reduces entropy while improving grammatical plausibility.

---

## Python implementation

```python
def valid_sequence(tokens):
    punct = {".", ",", ";", ":", "?", "!"}

    for i in range(len(tokens) - 1):
        if tokens[i] in punct and tokens[i+1] in punct:
            return False

    return True
```

---

# 4. Sentence-Structured Library

## Constraint

Every sentence must contain:

* exactly 15 words,
* followed by one punctuation mark.

Pattern:

```text
W W W W W W W W W W W W W W W P
```

Sentence count:

[
S = \left\lfloor \frac{N}{16} \right\rfloor
]

Total Library:

W^{15S}P^S

Approximation:

[
\approx 10^{1{,}035{,}639}
]

The Library loses vast amounts of entropy while gaining strong textual regularity.

Random pages now resemble primitive prose.

---

## Python generator

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

# 5. Grammar-Constrained Library

## Constraint

Sentences must satisfy grammatical templates.

Example:

```text
DET ADJ NOUN VERB DET NOUN .
```

Define vocabulary partitions:

* nouns,
* verbs,
* adjectives,
* adverbs,
* determiners,
* pronouns,
* prepositions.

---

## Combinatorics

If:

[
D,A,N,V
]

represent category counts, then one sentence template produces:

D\cdot A\cdot N\cdot V\cdot D\cdot N\cdot P

possible sentences.

A book with (S) such sentences gives:

[
(DANVDNP)^S
]

This reduction is enormous.

However, readability increases dramatically.

Random pages now resemble machine-generated language.

---

## Python implementation

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

# 6. Semantic-Constrained Library

## Constraint

Not all grammatically valid sentences are meaningful.

Introduce semantic neighborhoods.

Example:

```text
river ↔ water ↔ flow ↔ current
library ↔ books ↔ shelves ↔ archive
```

Words may only follow semantically compatible words.

This transforms the Library from a combinatoric explosion into a constrained semantic graph.

---

## Markov formulation

Let:

[
T_{ij}
]

be transition probability from token (i) to token (j).

Then valid books are paths through the semantic graph.

Approximate sequence count:

\lambda_{max}^N

where:

[
\lambda_{max}
]

is the dominant eigenvalue of the transition matrix.

This is a profound reduction.

Meaning emerges from spectral constraints.

---

## Python implementation

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

# 7. Topic-Coherent Library

## Constraint

Entire books must remain inside a thematic manifold.

Examples:

* cosmology,
* grief,
* mathematics,
* theology,
* medieval warfare.

This introduces long-range coherence.

Now the Library approximates actual literature.

---

## Information-theoretic interpretation

The original Borges Library maximizes entropy:

[
H_{max}
]

Every subsequent constraint reduces entropy:

[
H_1 > H_2 > H_3 > H_4
]

while increasing mutual information:

[
I(text;meaning)
]

The experiment demonstrates that human-readable language occupies an infinitesimally thin manifold inside the full combinatoric space of possible books.

---

# 8. Final Observation

The original Library is not terrifying because it contains all books.

It is terrifying because meaningful books are drowned inside an ocean of entropy.

Each constraint that is introduced in this article:

* decreases combinatoric volume
* increases semantic density
* and moves the Library closer to the tiny structured region inhabited by human thought

The true Library of meaning is not infinite.

It is an extraordinarily compressed island hidden inside Borges’ cosmic desert of symbols.
