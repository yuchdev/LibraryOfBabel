from babel_poc.generators.base import BookConfig
from babel_poc.generators.no_adjacent_punctuation import NoAdjacentPunctuationGenerator


def test_no_adjacent_punctuation(demo_words, demo_punctuation):
    gen = NoAdjacentPunctuationGenerator(demo_words, demo_punctuation)
    punct_set = set(demo_punctuation)
    config = BookConfig(
        mode_id="no-adjacent-punctuation",
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
