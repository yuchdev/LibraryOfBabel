from babel.vocabulary.sources import KNOWN_VOCABULARY_SOURCES


def test_known_sources_present():
    assert {"scowl", "wordnet", "wordfreq_25k", "subtlex_us"}.issubset(
        set(KNOWN_VOCABULARY_SOURCES)
    )


def test_wordnet_expected_files_include_pos_files():
    files = set(KNOWN_VOCABULARY_SOURCES["wordnet"].expected_files)
    assert {"words.txt", "nouns.txt", "verbs.txt", "adjectives.txt", "adverbs.txt"}.issubset(files)


def test_wordfreq_has_download_url():
    assert KNOWN_VOCABULARY_SOURCES["wordfreq_25k"].download_url


def test_sources_are_serializable():
    data = KNOWN_VOCABULARY_SOURCES["scowl"].model_dump()
    assert data["source_id"] == "scowl"
