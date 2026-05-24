import math

from babel_poc.generators.base import BookConfig
from babel_poc.generators.fixed_sentence import WORDS_PER_SENTENCE, FixedSentenceGenerator


def test_fixed_sentence_structure(demo_words, demo_punctuation):
    gen = FixedSentenceGenerator(demo_words, demo_punctuation)
    config = BookConfig(
        mode_id="fixed-sentence",
        seed="test-seed",
        pages=10,
        tokens_per_page=160,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )
    page = gen.generate_page(config, 0)
    tokens = page.tokens
    sentence_end_punct = set(gen.sentence_end_punctuation)
    for i, token in enumerate(tokens):
        pos_in_sentence = i % (WORDS_PER_SENTENCE + 1)
        if pos_in_sentence == WORDS_PER_SENTENCE:
            assert token in sentence_end_punct, f"Token at pos {i} should be punct, got {token!r}"
        else:
            assert token not in sentence_end_punct, (
                f"Token at pos {i} should be word, got {token!r}"
            )


def test_fixed_sentence_log10_size(demo_words, demo_punctuation):
    gen = FixedSentenceGenerator(demo_words, demo_punctuation)
    log10_sz = gen.log10_size(pages=1, tokens_per_page=16)
    expected = 15 * math.log10(len(demo_words)) + math.log10(3)
    assert abs(log10_sz - expected) < 0.01
