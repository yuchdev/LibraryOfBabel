from babel.generators.base import BookConfig
from babel.generators.constants import SHARED_PUNCTUATION
from babel.generators.semantic_constrained import SemanticConstrainedGenerator


def test_semantic_transitions_follow_graph(demo_words, demo_punctuation):
    gen = SemanticConstrainedGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed", tokens_per_page=32, vocabulary_id="demo")
    page = gen.generate_page(cfg, 0)
    for i in range(1, len(page.tokens)):
        assert page.tokens[i] in gen.adjacency[page.tokens[i - 1]]


def test_semantic_deterministic_lambda_and_punctuation(demo_words, demo_punctuation):
    gen_a = SemanticConstrainedGenerator(demo_words, demo_punctuation)
    gen_b = SemanticConstrainedGenerator(demo_words, demo_punctuation)
    assert gen_a.lambda_max == gen_b.lambda_max
    assert set(SHARED_PUNCTUATION).issubset(set(gen_a.nodes))


def test_semantic_page_boundary_is_deterministic(demo_words, demo_punctuation):
    gen = SemanticConstrainedGenerator(demo_words, demo_punctuation)
    cfg = BookConfig(mode_id=gen.mode_id, seed="seed", tokens_per_page=16, vocabulary_id="demo")
    page0 = gen.generate_page(cfg, 0)
    page1 = gen.generate_page(cfg, 1)
    assert page1.tokens[0] in gen.adjacency[page0.tokens[-1]]
