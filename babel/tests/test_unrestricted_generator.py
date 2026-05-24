import math

from babel.generators.base import BookConfig
from babel.generators.unrestricted_words import UnrestrictedWordsGenerator


def test_log10_size_small():
    """W=2, P=1, N=3 -> (2+1)^3 = 27"""
    gen = UnrestrictedWordsGenerator(["a", "b"], ["."])
    log10_sz = gen.log10_size(pages=1, tokens_per_page=3)
    assert math.isclose(log10_sz, math.log10(27), rel_tol=1e-9)


def test_generate_token_deterministic(demo_words, demo_punctuation):
    gen = UnrestrictedWordsGenerator(demo_words, demo_punctuation)
    t1 = gen.generate_token("seed1", 0)
    t2 = gen.generate_token("seed1", 0)
    assert t1 == t2


def test_generate_token_different_seeds(demo_words, demo_punctuation):
    gen = UnrestrictedWordsGenerator(demo_words, demo_punctuation)
    tokens_a = [gen.generate_token("seed_a", i) for i in range(50)]
    tokens_b = [gen.generate_token("seed_b", i) for i in range(50)]
    assert tokens_a != tokens_b


def test_generate_page_length(demo_words, demo_punctuation):
    gen = UnrestrictedWordsGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="unrestricted-words",
        seed="test",
        pages=10,
        tokens_per_page=50,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page = gen.generate_page(config, 0)
    assert len(page.tokens) == 50


def test_generate_page_only_generates_one_page(demo_words, demo_punctuation):
    gen = UnrestrictedWordsGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="unrestricted-words",
        seed="test",
        pages=410,
        tokens_per_page=320,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page = gen.generate_page(config, 5)
    assert len(page.tokens) == 320
