from typer.testing import CliRunner

from babel.cli import app


def test_info_lists_stage_metadata():
    runner = CliRunner()
    result = runner.invoke(app, ["info"])
    assert result.exit_code == 0
    assert "Stage 0" in result.output
    assert "formula" in result.output
