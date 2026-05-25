from babel.generators.base import BookConfig
from babel.generators.constants import SHARED_PUNCTUATION
from babel.generators.topic_coherent import TopicCoherentGenerator


def test_topic_selection_is_deterministic(demo_words, demo_punctuation):
    gen = TopicCoherentGenerator(demo_words, demo_punctuation)
    assert gen._select_topic("seed-a") == gen._select_topic("seed-a")


def test_different_seeds_can_select_different_topics(demo_words, demo_punctuation):
    gen = TopicCoherentGenerator(demo_words, demo_punctuation)
    assert gen._select_topic("seed-a") != gen._select_topic("seed-b")


def test_generated_tokens_are_from_selected_topic_plus_punctuation(
    demo_words, demo_punctuation
):
    gen = TopicCoherentGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed-a", tokens_per_page=20, vocabulary_id="demo")
    page = gen.generate_page(cfg, 0)
    allowed = set(gen._get_book_vocab("seed-a"))
    assert all(token in allowed for token in page.tokens)
    assert set(SHARED_PUNCTUATION).issubset(allowed)
