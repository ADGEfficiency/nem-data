from click.testing import CliRunner
from nemdata.cli import cli


def test_cli_help():
  runner = CliRunner()
  result = runner.invoke(cli, ['--help'])
  assert result.exit_code == 0
