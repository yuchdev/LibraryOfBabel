import pytest
from typer.testing import CliRunner

from babel.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_info_command(runner):
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Borges" in result.output


def test_vocab_info_command(runner, demo_vocab_file):
    result = runner.invoke(app, ["vocab-info", "--vocab", str(demo_vocab_file)])
    assert result.exit_code == 0
    assert "Words loaded" in result.output


def test_metrics_command(runner, demo_vocab_file):
    result = runner.invoke(
        app,
        [
            "metrics",
            "--mode",
            "word-based",
            "--vocab",
            str(demo_vocab_file),
        ],
    )
    assert result.exit_code == 0
    assert "log10" in result.output


def test_page_command(runner, demo_vocab_file):
    result = runner.invoke(
        app,
        [
            "page",
            "--mode",
            "sentence-structured",
            "--vocab",
            str(demo_vocab_file),
            "--seed",
            "test-seed",
            "--page",
            "0",
        ],
    )
    assert result.exit_code == 0
    assert "Page" in result.output


def test_compare_command(runner, demo_vocab_file):
    result = runner.invoke(app, ["compare", "--vocab", str(demo_vocab_file)])
    assert result.exit_code == 0
    assert "Borges" in result.output


def test_vocab_info_missing_file(runner):
    result = runner.invoke(app, ["vocab-info", "--vocab", "/nonexistent/path.txt"])
    assert result.exit_code != 0
