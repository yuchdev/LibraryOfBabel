from pathlib import Path

from babel.vocabulary.loader import load_pos_vocab


def test_load_pos_vocab_wordnet_style_files(tmp_path: Path):
    (tmp_path / "nouns.txt").write_text("library\nbook\n", encoding="utf-8")
    (tmp_path / "verbs.txt").write_text("contains\n", encoding="utf-8")
    (tmp_path / "adjectives.txt").write_text("ancient\n", encoding="utf-8")
    (tmp_path / "adverbs.txt").write_text("slowly\n", encoding="utf-8")
    loaded = load_pos_vocab(tmp_path)
    assert loaded["NOUN"] == ["book", "library"]
    assert loaded["VERB"] == ["contains"]
    assert loaded["ADJ"] == ["ancient"]
    assert loaded["ADV"] == ["slowly"]
