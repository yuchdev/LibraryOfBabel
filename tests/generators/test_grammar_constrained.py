import math

import pytest

from babel.generators.base import BookConfig
from babel.generators.constants import SHARED_PUNCTUATION, TOKEN_SLOTS_PER_BOOK
from babel.generators.grammar_constrained import DEFAULT_TEMPLATE, GrammarConstrainedGenerator


def test_default_template_and_punctuation(demo_words, demo_punctuation):
    gen = GrammarConstrainedGenerator(demo_words, demo_punctuation)
    assert gen.template == DEFAULT_TEMPLATE
    assert gen.pos_vocab["PUNCT"] == SHARED_PUNCTUATION


def test_formula_uses_category_product(demo_words, demo_punctuation):
    gen = GrammarConstrainedGenerator(demo_words, demo_punctuation)
    r = TOKEN_SLOTS_PER_BOOK // len(DEFAULT_TEMPLATE)
    expected = r * sum(math.log10(len(gen.pos_vocab[tag])) for tag in DEFAULT_TEMPLATE)
    assert math.isclose(gen.log10_size(), expected, rel_tol=1e-9)


def test_positions_follow_template(demo_words, demo_punctuation):
    gen = GrammarConstrainedGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed", tokens_per_page=14, vocabulary_id="demo")
    page = gen.generate_page(cfg, 0)
    for idx, token in enumerate(page.tokens):
        tag = DEFAULT_TEMPLATE[idx % len(DEFAULT_TEMPLATE)]
        assert token in gen.pos_vocab[tag]


def test_empty_category_raises(demo_words, demo_punctuation):
    gen = GrammarConstrainedGenerator(demo_words, demo_punctuation, pos_vocab={"VERB": []})
    with pytest.raises(ValueError):
        gen.generate_token("seed", 3)
