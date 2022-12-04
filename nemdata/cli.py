import click
import pandas as pd

from nemdata import mmsdm
from nemdata.config import DEFAULT_BASE_DIR
from nemdata.nemde import download_nemde


@click.command()
@click.option("--start", "-s", default="2018-01", help="start date (YYYY-MM)")
@click.option("--end", "-e", default="2018-03", help="end date (incusive) (YYYY-MM)")
@click.option(
    "--report",
    "-r",
    help="nemde, " + ", ".join(mmsdm.reports.keys()),
)
def cli(start, end, report):
    """nem-data is a tool to access NEM data"""
    click.echo("Hello from nem-data :)\n")
    print(f"Starting downloads for {report}")
    download(start, end, report)


def download(start, end, report_id, base_dir=DEFAULT_BASE_DIR):
    reports = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
    }
    return reports[report_id](start, end, report_id, base_dir)


if __name__ == "__main__":
    cli()
