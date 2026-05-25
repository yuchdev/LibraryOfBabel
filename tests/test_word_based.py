import math

from babel.generators.base import BookConfig
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.word_based import WordBasedGenerator


def test_log10_size_uses_theoretical_token_slots():
    gen = WordBasedGenerator(["a", "b"], SHARED_PUNCTUATION)
    log10_sz = gen.log10_size(pages=1, tokens_per_page=3)
    expected = TOKEN_SLOTS_PER_BOOK * math.log10(2 + len(SHARED_PUNCTUATION))
    assert math.isclose(log10_sz, expected, rel_tol=1e-9)


def test_generate_token_deterministic(demo_words, demo_punctuation):
    gen = WordBasedGenerator(demo_words, demo_punctuation)
    t1 = gen.generate_token("seed1", 0)
    t2 = gen.generate_token("seed1", 0)
    assert t1 == t2


def test_generate_token_different_seeds(demo_words, demo_punctuation):
    gen = WordBasedGenerator(demo_words, demo_punctuation)
    tokens_a = [gen.generate_token("seed_a", i) for i in range(50)]
    tokens_b = [gen.generate_token("seed_b", i) for i in range(50)]
    assert tokens_a != tokens_b


def test_generate_page_length(demo_words, demo_punctuation):
    gen = WordBasedGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="word-based",
        seed="test",
        pages=10,
        tokens_per_page=50,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page = gen.generate_page(config, 0)
    assert len(page.tokens) == 50


def test_generate_page_only_generates_one_page(demo_words, demo_punctuation):
    gen = WordBasedGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="word-based",
        seed="test",
        pages=410,
        tokens_per_page=320,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page = gen.generate_page(config, 5)
    assert len(page.tokens) == 320


def test_generate_token_domain_is_words_plus_shared_punctuation(
    demo_words, demo_punctuation
):
    gen = WordBasedGenerator(demo_words, demo_punctuation)
    token = gen.generate_token("seed", 3)
    assert token in (set(demo_words) | set(SHARED_PUNCTUATION))
