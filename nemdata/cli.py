import pathlib
import typing

import click
import pandas as pd
from rich import print

from nemdata import mmsdm
from nemdata.config import DEFAULT_BASE_DIR
from nemdata.nemde import download_nemde


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


def download(
    start: str,
    end: str,
    table_name: str,
    base_directory: pathlib.Path = DEFAULT_BASE_DIR,
    dry_run: bool = False,
) -> pd.DataFrame:
    print(f"[bold green]Downloader[/]: table: {table_name}")
    tables: dict[str, typing.Callable] = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
        "demand": mmsdm.download_mmsdm,
        "interconnectors": mmsdm.download_mmsdm,
    }
    return tables[table_name](
        start,
        end,
        table_name=table_name,
        base_directory=base_directory,
        dry_run=dry_run,
    )


if __name__ == "__main__":
    cli()
