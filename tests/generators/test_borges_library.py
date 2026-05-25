import math

from babel.generators.base import BookConfig
from babel.generators.borges_library import BorgesLibraryGenerator
from babel.generators.constants import CHARS_PER_BOOK, ENGLISH_CHARACTER_ALPHABET


def test_borges_alphabet_exact(demo_words, demo_punctuation):
    gen = BorgesLibraryGenerator(demo_words, demo_punctuation)
    assert gen.alphabet == ENGLISH_CHARACTER_ALPHABET


def test_borges_formula(demo_words, demo_punctuation):
    gen = BorgesLibraryGenerator(demo_words, demo_punctuation)
    assert math.isclose(gen.log10_size(), CHARS_PER_BOOK * math.log10(31), rel_tol=1e-9)


def test_borges_page_deterministic_and_domain(demo_words, demo_punctuation):
    gen = BorgesLibraryGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed", tokens_per_page=64, vocabulary_id="demo")
    page_a = gen.generate_page(cfg, 0)
    page_b = gen.generate_page(cfg, 0)
    assert page_a.tokens == page_b.tokens
    assert set(page_a.tokens).issubset(set(ENGLISH_CHARACTER_ALPHABET))


def test_borges_page_indices_use_different_positions(demo_words, demo_punctuation):
    gen = BorgesLibraryGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed", tokens_per_page=64, vocabulary_id="demo")
    page0 = gen.generate_page(cfg, 0)
    page1 = gen.generate_page(cfg, 1)
    assert page0.tokens != page1.tokens
