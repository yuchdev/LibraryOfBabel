from pathlib import Path

import pytest

DEMO_VOCAB_WORDS = [
    "the",
    "a",
    "an",
    "this",
    "that",
    "some",
    "dark",
    "old",
    "river",
    "house",
    "mirror",
    "memory",
    "library",
    "book",
    "contains",
    "reflects",
    "holds",
    "reveals",
    "time",
    "light",
    "night",
    "wind",
    "path",
    "door",
    "stone",
    "cloud",
    "ancient",
    "bright",
    "deep",
    "hides",
]


@pytest.fixture
def demo_vocab_file(tmp_path: Path) -> Path:
    vocab_file = tmp_path / "vocab.txt"
    vocab_file.write_text("\n".join(DEMO_VOCAB_WORDS) + "\n", encoding="utf-8")
    return vocab_file


@pytest.fixture
def demo_words() -> list[str]:
    return sorted(DEMO_VOCAB_WORDS)


@pytest.fixture
def demo_punctuation() -> list[str]:
    return [".", ",", ";", ":", "?", "!"]
