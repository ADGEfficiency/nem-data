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
import aiohttp


async def download_raw_zip_async(uow: m.UOW, verbose: bool, attempts=5):
    connector = aiohttp.TCPConnector(limit_per_host=2)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
    }
    import random

    async with aiohttp.ClientSession(connector=connector) as session:
        for attempt in range(attempts):
            async with session.get(
                uow.url, raise_for_status=False, headers=headers
            ) as response:
                try:
                    assert response.status == 200
                    print(f"[green] SUCCESS DOWNLOADED[/] {uow.raw_zip}")
                    content = await response.read()
                    #  async write of file to disk
                    async with aiofiles.open(uow.raw_zip, mode="wb") as f:
                        await f.write(content)
                        print(f"[green] SUCCESS WRITE[/] {uow.raw_zip}")
                    return "success"

                except AssertionError:
                    print(
                        f"[red] FAILED DOWNLOADED[/] attempt {attempt}/{attempts} {uow.raw_zip}"
                    )
                    await asyncio.sleep(random.random() * attempt)

    return "fail"


async def download_raw_zips_async(urls, verbose):
    routines = [download_raw_zip_async(url, verbose) for url in urls]
    results = await asyncio.gather(*routines)
    successes = len(list(filter(lambda x: x == "success", results)))
    print(f"[green]DOWNLOADED[/] [blue]{successes}/{len(routines)} zip files[/]")


def download_raw_zip(uow, verbose):
    with httpx.Client() as client:
        response = client.get(uow.url)
        assert response.status_code == 200
    uow.raw_zip.write_bytes(response.content)
    print(f"[green] SUCCESS DOWNLOADED[/] {uow.raw_zip}")
    return "success"


def download_raw_zips(uows, verbose):
    results = [download_raw_zip(uow, verbose) for uow in uows]
    successes = len(list(filter(lambda x: x == "success", results)))
    print(f"[green]DOWNLOADED[/] [blue]{successes}/{len(results)} zip files[/]")


@app.command()
def cli(
    start: datetime,
    end: datetime,
    table: str,
    verbose: bool = typer.Option(False, show_default=True),
    use_async: bool = typer.Option(False, show_default=True),
    use_multiprocess: bool = typer.Option(True, show_default=True),
):
    print(":wave: from [bold green]nem-data[/] [green]^^[/]\n")

    #  get a class for this Table
    table = get_table(table)

    #  list of urls to download data from
    urls = table.create_urls(start, end)

    #  raw data stage
    #  saves to a `raw.zip` file (one per url)
    print(f"[green]DOWNLOADING[/] [blue]{len(urls)} urls[/]")
    if use_async:
        print("async backend")
        asyncio.run(download_raw_zips_async(urls, verbose))
    else:
        print("sync backend")
        download_raw_zips(urls, verbose)

    print(f"[green]PROCESSING[/] [blue]{len(urls)} zip files[/]")
    process_raw_datas(urls)


def run_cli() -> None:
    app()
