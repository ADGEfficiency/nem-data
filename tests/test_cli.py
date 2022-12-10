from click.testing import CliRunner

from nemdata.cli import cli


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


def test_cli_download() -> None:
    runner = CliRunner()
    result = runner.invoke(
        cli, ["--table", "trading-price", "-s", "2020-01", "-e", "2020-01", "--dry-run"]
    )
    assert result.exit_code == 0
