import click
import pandas as pd

from nemdata.mmsdm import download_mmsdm
from nemdata.mmsdm import reports as mmsdm_reports
from nemdata.nemde import download_nemde


@click.command()
@click.option("--start", "-s", default="2018-01", help="start date (YYYY-MM)")
@click.option("--end", "-e", default="2018-03", help="end date (incusive) (YYYY-MM)")
@click.option(
    "--reports",
    "-r",
    multiple=True,
    default=["nemde"],
    help="nemde, " + ", ".join(mmsdm_reports.keys()),
)
def cli(start, end, reports):
    """nem-data is a tool to access NEM data"""
    click.echo("Hello from nem-data :)\n")
    for report in reports:
        print(f" starting downloads for {report}")
        download(start, end, report)


def download(start, end, report_id):
    reports = {"nemde": download_nemde, "mmsdm": download_mmsdm}
    return reports[report_id](start, end, report_id)


if __name__ == "__main__":
    cli()
