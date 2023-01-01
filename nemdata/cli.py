import click
from rich import print

from nemdata import mmsdm
from nemdata.downloader import download


@click.command()
@click.option(
    "--table",
    "-t",
    help="nemde, " + ", ".join([table.name for table in mmsdm.mmsdm_tables]),
)
@click.option("--start", "-s", default="2018-01", help="start date (YYYY-MM)")
@click.option("--end", "-e", default="2018-03", help="end date (incusive) (YYYY-MM)")
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="whether to save downloaded data to disk",
)
def cli(start: str, end: str, table: str, dry_run: bool) -> None:
    """nemdata is a tool to access NEM data from AEMO."""
    print(":wave: from nemdata\n")
    download(start, end, table, dry_run=dry_run)


if __name__ == "__main__":
    cli()
