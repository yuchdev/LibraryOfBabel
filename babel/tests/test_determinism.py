import pytest

from babel.generators.base import BookConfig
from babel.generators.fixed_sentence import FixedSentenceGenerator
from babel.generators.no_adjacent_punctuation import NoAdjacentPunctuationGenerator
from babel.generators.pos_template import POSTemplateGenerator
from babel.generators.unrestricted_words import UnrestrictedWordsGenerator


def _make_config(mode_id: str, seed: str, demo_punctuation) -> BookConfig:
    return BookConfig(
        mode_id=mode_id,
        seed=seed,
        pages=10,
        tokens_per_page=50,
        vocabulary_id="demo",
        punctuation=demo_punctuation,
    )


@pytest.mark.parametrize(
    ("GeneratorClass", "mode_id"),
    [
        (UnrestrictedWordsGenerator, "unrestricted-words"),
        (FixedSentenceGenerator, "fixed-sentence"),
        (NoAdjacentPunctuationGenerator, "no-adjacent-punctuation"),
        (POSTemplateGenerator, "pos-template"),
    ],
)
def test_same_seed_same_page(GeneratorClass, mode_id, demo_words, demo_punctuation):
    gen = GeneratorClass(demo_words, demo_punctuation)
    config = _make_config(mode_id, "fixed-seed", demo_punctuation)
    page1 = gen.generate_page(config, 3)
    page2 = gen.generate_page(config, 3)
    assert page1.tokens == page2.tokens


@pytest.mark.parametrize(
    ("GeneratorClass", "mode_id"),
    [
        (UnrestrictedWordsGenerator, "unrestricted-words"),
        (FixedSentenceGenerator, "fixed-sentence"),
        (NoAdjacentPunctuationGenerator, "no-adjacent-punctuation"),
        (POSTemplateGenerator, "pos-template"),
    ],
)
def test_different_seeds_different_pages(
    GeneratorClass, mode_id, demo_words, demo_punctuation
):
    gen = GeneratorClass(demo_words, demo_punctuation)
    config_a = _make_config(mode_id, "seed-alpha", demo_punctuation)
    config_b = _make_config(mode_id, "seed-beta", demo_punctuation)
    page_a = gen.generate_page(config_a, 0)
    page_b = gen.generate_page(config_b, 0)
    assert page_a.tokens != page_b.tokens


@pytest.mark.parametrize(
    ("GeneratorClass", "mode_id"),
    [
        (UnrestrictedWordsGenerator, "unrestricted-words"),
        (FixedSentenceGenerator, "fixed-sentence"),
        (NoAdjacentPunctuationGenerator, "no-adjacent-punctuation"),
        (POSTemplateGenerator, "pos-template"),
    ],
)
def test_different_page_indices(GeneratorClass, mode_id, demo_words, demo_punctuation):
    gen = GeneratorClass(demo_words, demo_punctuation)
    config = _make_config(mode_id, "test-seed", demo_punctuation)
    page0 = gen.generate_page(config, 0)
    page1 = gen.generate_page(config, 1)
    assert page0.tokens != page1.tokens
