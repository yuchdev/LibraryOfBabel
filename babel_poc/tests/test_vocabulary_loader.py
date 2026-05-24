from pathlib import Path

from babel_poc.vocabulary.loader import load_words
from babel_poc.vocabulary.normalizer import normalize_words


def test_load_words_basic(demo_vocab_file: Path):
    words = load_words(demo_vocab_file)
    assert isinstance(words, list)
    assert len(words) > 0
    assert words == sorted(words)


def test_load_words_deduplication(tmp_path: Path):
    vocab_file = tmp_path / "dup.txt"
    vocab_file.write_text("apple\napple\nbanana\n", encoding="utf-8")
    words = load_words(vocab_file)
    assert words.count("apple") == 1
    assert words.count("banana") == 1


def test_load_words_ignores_comments(tmp_path: Path):
    vocab_file = tmp_path / "comments.txt"
    vocab_file.write_text("# comment\napple\n# another\nbanana\n", encoding="utf-8")
    words = load_words(vocab_file)
    assert "# comment" not in words
    assert "apple" in words
    assert "banana" in words


def test_load_words_ignores_empty_lines(tmp_path: Path):
    vocab_file = tmp_path / "empty.txt"
    vocab_file.write_text("apple\n\n\nbanana\n", encoding="utf-8")
    words = load_words(vocab_file)
    assert "" not in words


def test_normalize_words_lowercase():
    words = normalize_words(["Apple", "BANANA", "Cherry"])
    assert "apple" in words
    assert "banana" in words
    assert "cherry" in words


def test_normalize_words_dedup():
    words = normalize_words(["apple", "Apple", "APPLE"])
    assert words.count("apple") == 1


def test_normalize_words_sorted():
    words = normalize_words(["cherry", "apple", "banana"])
    assert words == sorted(words)


def test_normalize_words_reject_spaces():
    words = normalize_words(["good word", "hello", "bad word"], reject_spaces=True)
    assert "hello" in words
    assert "good word" not in words
    assert "bad word" not in words
