import click
import pandas as pd

from nemdata import mmsdm
from nemdata.nemde import download_nemde


@click.command()
@click.option("--start", "-s", default="2018-01", help="start date (YYYY-MM)")
@click.option("--end", "-e", default="2018-03", help="end date (incusive) (YYYY-MM)")
@click.option(
    "--reports",
    "-r",
    multiple=True,
    default=["nemde"],
    help="nemde, " + ", ".join(mmsdm.reports.keys()),
)
def cli(start, end, reports):
    """nem-data is a tool to access NEM data"""
    click.echo("Hello from nem-data :)\n")
    for report in reports:
        print(f"starting downloads for {report}")
        download(start, end, report)


def download(start, end, report_id):
    reports = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
    }
    return reports[report_id](start, end, report_id)


if __name__ == "__main__":
    cli()
