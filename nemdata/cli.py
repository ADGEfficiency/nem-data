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
def cli(start: str, end: str, report: str) -> None:
    """nemdata is a tool to access NEM data from AEMO."""
    print(":wave: from nemdata\n")
    download(start, end, report)


def download(
    start: str,
    end: str,
    table_name: str,
    base_directory: pathlib.Path = DEFAULT_BASE_DIR,
) -> pd.DataFrame:
    print(f"[bold green]Downloader[/]: table: {table_name}")
    tables: dict[str, typing.Callable] = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
    }
    return tables[table_name](
        start, end, table_name=table_name, base_directory=base_directory
    )


if __name__ == "__main__":
    cli()
