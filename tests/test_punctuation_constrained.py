from babel.generators.base import BookConfig
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.punctuation_constrained import PunctuationConstrainedGenerator
from babel.mathlib.combinatorics import log10_no_adjacent_punct


def test_no_adjacent_punctuation(demo_words, demo_punctuation):
    gen = PunctuationConstrainedGenerator(demo_words, demo_punctuation)
    punct_set = set(demo_punctuation)
    config = BookConfig(
        mode_id="punctuation-constrained",
        seed="test-seed",
        pages=10,
        tokens_per_page=100,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    for page_idx in range(5):
        page = gen.generate_page(config, page_idx)
        tokens = page.tokens
        for i in range(len(tokens) - 1):
            assert not (tokens[i] in punct_set and tokens[i + 1] in punct_set), (
                f"Adjacent punctuation at positions {i}, {i + 1}: "
                f"{tokens[i]!r}, {tokens[i + 1]!r}"
            )


def test_boundary_no_adjacent_punctuation(demo_words, demo_punctuation):
    gen = PunctuationConstrainedGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="punctuation-constrained",
        seed="test-seed",
        pages=10,
        tokens_per_page=64,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page0 = gen.generate_page(config, 0)
    page1 = gen.generate_page(config, 1)
    assert not (page0.tokens[-1] in SHARED_PUNCTUATION and page1.tokens[0] in SHARED_PUNCTUATION)


def test_formula_uses_theoretical_token_slots(demo_words, demo_punctuation):
    gen = PunctuationConstrainedGenerator(demo_words, demo_punctuation)
    assert gen.log10_size(pages=1, tokens_per_page=3) == log10_no_adjacent_punct(
        TOKEN_SLOTS_PER_BOOK,
        len(demo_words),
        len(SHARED_PUNCTUATION),
    )
