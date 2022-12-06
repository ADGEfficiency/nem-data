import click
from rich import print

from nemdata import mmsdm
from nemdata.config import DEFAULT_BASE_DIR
from nemdata.nemde import download_nemde


@click.command()
@click.option(
    "--report",
    "-r",
    help="nemde, " + ", ".join(mmsdm.reports.keys()),
)
@click.option("--start", "-s", default="2018-01", help="start date (YYYY-MM)")
@click.option("--end", "-e", default="2018-03", help="end date (incusive) (YYYY-MM)")
def cli(start, end, report):
    """nemdata is a tool to access NEM data"""
    print(":wave: from nemdata\n")
    download(start, end, report)


def download(start, end, report_id, base_dir=DEFAULT_BASE_DIR):
    print(f"[bold green]Downloader[/]: {report_id}")
    reports = {
        "nemde": download_nemde,
        "trading-price": mmsdm.download_mmsdm,
        "unit-scada": mmsdm.download_mmsdm,
    }
    return reports[report_id](start, end, report_id, base_dir)


if __name__ == "__main__":
    cli()
