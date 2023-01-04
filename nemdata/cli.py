import click
from rich import print

from nemdata import mmsdm
from nemdata.downloader import download


@click.command()
@click.option(
    "--table",
    "-t",
    help="Available tables: nemde, "
    + ", ".join([table.name for table in mmsdm.mmsdm_tables])
    + ".",
)
@click.option(
    "--start",
    "-s",
    default="2018-01",
    help="Start date (YYYY-MM or YYYY-MM-DD for NEMDE).",
)
@click.option(
    "--end",
    "-e",
    default="2018-03",
    help="End date (incusive) (YYYY-MM or YYYY-MM-DD for NEMDE).",
)
@click.option(
    "--dry-run/--no-dry-run",
    default=False,
    help="Whether to save downloaded data to disk.",
)
def cli(start: str, end: str, table: str, dry_run: bool) -> None:
    """Downloads NEM data from AEMO."""
    print(":wave: from nemdata\n")
    download(start, end, table, dry_run=dry_run)
