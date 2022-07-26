import asyncio
from datetime import datetime
from typing import List

from rich import print
import aiofiles
import httpx
import typer

from nemdata.urls import create_urls
from nemdata.tables import get_table
from nemdata import models as m

app = typer.Typer()

import random


async def download_raw_zip(uow: m.UOW):

    #  async download of the file
    success = False
    for attempt in range(1, 5):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(uow.url)
                assert response.status_code == 200
                success = True
                print(f"\n[green] SUCCESS DOWNLOAD[/]\n {uow}")
        except AssertionError:
            print(f"\n[red] FAILED DOWNLOAD[/]\n {uow}")
            print(response.content)
            asyncio.sleep(attempt)

    #  possible for OK failures (data actually doesn't exist) to slip through here
    #  TODO

    #  async write of file to disk
    async with aiofiles.open(uow.raw_fi, mode="wb") as f:
        await f.write(response.content)


async def download_raw_zips(urls):
    routines = [download_raw_zip(url) for url in urls]
    await asyncio.gather(*routines)
    print(f" downloaded [green]{len(routines)} zip files[/]")


from nemdata.pipeline import process_raw_datas


@app.command()
def cli(start: datetime, end: datetime, table: str):
    print(":wave: from [bold green]nem-data[/] [green]^^[/]\n")

    #  get a class for this Table
    table = get_table(table)

    #  list of urls to download data from
    urls = create_urls(start, end, table)

    #  raw data stage
    #  saves to a `raw.zip` file (one per url)
    asyncio.run(download_raw_zips(urls))

    #  processed data stage
    process_raw_datas(urls)


def run_cli() -> None:
    app()
