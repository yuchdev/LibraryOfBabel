from babel.generators.borges_library import BorgesLibraryGenerator
from babel.generators.grammar_constrained import GrammarConstrainedGenerator
from babel.generators.punctuation_constrained import PunctuationConstrainedGenerator
from babel.generators.semantic_constrained import SemanticConstrainedGenerator
from babel.generators.sentence_structured import SentenceStructuredGenerator
from babel.generators.topic_coherent import TopicCoherentGenerator
from babel.generators.word_based import WordBasedGenerator


def test_all_models_expose_metadata(demo_words, demo_punctuation):
    generators = [
        BorgesLibraryGenerator(demo_words, demo_punctuation),
        WordBasedGenerator(demo_words, demo_punctuation),
        PunctuationConstrainedGenerator(demo_words, demo_punctuation),
        SentenceStructuredGenerator(demo_words, demo_punctuation),
        GrammarConstrainedGenerator(demo_words, demo_punctuation),
        SemanticConstrainedGenerator(demo_words, demo_punctuation),
        TopicCoherentGenerator(demo_words, demo_punctuation),
    ]
    for gen in generators:
        assert gen.metadata.mode_id == gen.mode_id
        assert gen.metadata.formula
        assert gen.metadata.display_name.startswith("Stage")
