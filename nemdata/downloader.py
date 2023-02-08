import pathlib
import typing

import pandas as pd
from rich import print

from nemdata import mmsdm
from nemdata.config import DEFAULT_BASE_DIR
from nemdata.nemde import download_nemde


def download(
    start: str,
    end: str,
    table: str,
    base_directory: pathlib.Path = DEFAULT_BASE_DIR,
    dry_run: bool = False,
) -> pd.DataFrame:
    print(f"[bold green]nemdata download[/]: {table}")
    tables: dict[str, typing.Callable] = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "dispatch-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
        "demand": mmsdm.download_mmsdm,
        "interconnectors": mmsdm.download_mmsdm,
    }
    return tables[table](
        start,
        end,
        table_name=table,
        base_directory=base_directory,
        dry_run=dry_run,
    )
