import asyncio
from datetime import datetime
from typing import List

from rich import print
import aiofiles
import httpx
import typer

from nemdata.pipeline import process_raw_datas
from nemdata.tables import get_table
from nemdata import models as m

app = typer.Typer()

import random


async def download_raw_zip(uow: m.UOW, verbose: bool):

    #  async download of the file
    for attempt in range(1, 5):

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(uow.url)
                assert response.status_code == 200
                print(f"[green] SUCCESS DOWNLOADED[/] {uow.raw_zip}")
                break

            except AssertionError:
                if verbose:
                    print(f"[red] FAILED DOWNLOADED[/] {uow.raw_zip}")
                    await asyncio.sleep(attempt**2)

    #  async write of file to disk
    if response.status_code == 200:
        async with aiofiles.open(uow.raw_zip, mode="wb") as f:
            await f.write(response.content)

    return "success"


async def download_raw_zips(urls, verbose):
    routines = [download_raw_zip(url, verbose) for url in urls]
    results = await asyncio.gather(*routines, return_exceptions=True)
    successes = len(list(filter(lambda x: x == "success", results)))
    print(f"[green]DOWNLOADED[/] [blue]{successes}/{len(routines)} zip files[/]")


@app.command()
def cli(
    start: datetime,
    end: datetime,
    table: str,
    verbose: bool = typer.Option(False, show_default=True),
):
    print(":wave: from [bold green]nem-data[/] [green]^^[/]\n")

    #  get a class for this Table
    table = get_table(table)

    #  list of urls to download data from
    urls = table.create_urls(start, end)

    #  raw data stage
    #  saves to a `raw.zip` file (one per url)
    print(f"[green]DOWNLOADING[/] [blue]{len(urls)} urls[/]")
    asyncio.run(download_raw_zips(urls, verbose))

    print(f"[green]PROCESSING[/] [blue]{len(urls)} zip files[/]")
    process_raw_datas(urls)


def run_cli() -> None:
    app()
