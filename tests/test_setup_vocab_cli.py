"""Tests for setup-vocab and vocab-list-sources CLI commands."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from babel.cli import app
from babel.vocabulary.manifest import InstalledVocabulary


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


FAKE_ENTRY = InstalledVocabulary(
    source_id="wordfreq_25k",
    vocabulary_id="wordfreq_25k",
    path=Path("/fake/vocab/wordfreq/words.txt"),
    word_count=25000,
    installed_at="2024-01-01T00:00:00+00:00",
    source_url="https://example.com/words.json",
    license_name="CC BY 4.0",
    sha256="deadbeef",
)


# ---------------------------------------------------------------------------
# vocab-list-sources
# ---------------------------------------------------------------------------


def test_vocab_list_sources_shows_all_sources(runner: CliRunner) -> None:
    result = runner.invoke(app, ["vocab-list-sources"])
    assert result.exit_code == 0
    assert "scowl" in result.output
    assert "wordfreq" in result.output  # "wordfreq_25k" may be truncated by Rich table layout
    assert "wordnet" in result.output
    assert "subtlex_us" in result.output


def test_vocab_list_sources_shows_setup_hint(runner: CliRunner) -> None:
    result = runner.invoke(app, ["vocab-list-sources"])
    assert result.exit_code == 0
    assert "setup-vocab" in result.output


# ---------------------------------------------------------------------------
# setup-vocab
# ---------------------------------------------------------------------------


def test_setup_vocab_no_args_exits_nonzero(runner: CliRunner) -> None:
    result = runner.invoke(app, ["setup-vocab"])
    assert result.exit_code != 0


def test_setup_vocab_unknown_source_exits_nonzero(runner: CliRunner) -> None:
    result = runner.invoke(app, ["setup-vocab", "--source", "totally_unknown_source"])
    assert result.exit_code != 0


def test_setup_vocab_source_with_mocked_installer(runner: CliRunner) -> None:
    with patch("babel.cli.install_source", return_value=FAKE_ENTRY) as mock_install:
        result = runner.invoke(app, ["setup-vocab", "--source", "wordfreq_25k"])
    assert result.exit_code == 0
    assert "wordfreq_25k" in result.output
    mock_install.assert_called_once_with("wordfreq_25k", force=False)


def test_setup_vocab_all_with_mocked_installer(runner: CliRunner) -> None:
    with patch("babel.cli.install_all_sources", return_value=[FAKE_ENTRY]) as mock_install:
        result = runner.invoke(app, ["setup-vocab", "--all"])
    assert result.exit_code == 0
    assert "wordfreq_25k" in result.output
    mock_install.assert_called_once_with(force=False)


def test_setup_vocab_force_flag_passed(runner: CliRunner) -> None:
    with patch("babel.cli.install_source", return_value=FAKE_ENTRY) as mock_install:
        runner.invoke(app, ["setup-vocab", "--source", "wordfreq_25k", "--force"])
    mock_install.assert_called_once_with("wordfreq_25k", force=True)


def test_setup_vocab_no_downloadable_sources(runner: CliRunner) -> None:
    with patch("babel.cli.install_all_sources", return_value=[]):
        result = runner.invoke(app, ["setup-vocab", "--all"])
    assert result.exit_code == 0
    assert "No sources" in result.output or "no sources" in result.output.lower()


# ---------------------------------------------------------------------------
# page command — uses installed vocabulary when --vocab is omitted
# ---------------------------------------------------------------------------


def test_page_without_vocab_finds_installed(
    runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """page command must work when an installed vocabulary exists."""
    source_dir = tmp_path / "scowl"
    source_dir.mkdir()
    words = [
        "the", "a", "an", "this", "that", "some", "dark", "old", "river", "house",
        "mirror", "memory", "library", "book", "contains", "reflects", "holds",
        "reveals", "time", "light", "night", "wind", "path", "door", "stone",
        "cloud", "ancient", "bright", "deep", "hides",
    ]
    (source_dir / "words.txt").write_text("\n".join(words) + "\n", encoding="utf-8")

    import babel.vocabulary.discovery as disc

    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", tmp_path)

    result = runner.invoke(
        app,
        ["page", "--mode", "sentence-structured", "--seed", "test", "--page", "0"],
    )
    assert result.exit_code == 0
    assert "Page" in result.output


def test_page_without_vocab_no_default_shows_error(
    runner: CliRunner, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """page command must show a clear error when no vocabulary is available."""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    import babel.vocabulary.discovery as disc

    monkeypatch.setattr(disc, "DEFAULT_VOCAB_DIR", empty_dir)

    result = runner.invoke(app, ["page", "--mode", "sentence-structured"])
    assert result.exit_code != 0
    assert "setup-vocab" in result.output
