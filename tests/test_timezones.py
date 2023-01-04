import pathlib

import pandas as pd

from nemdata.cli import download
from nemdata.loader import load


def test_timezones(base_dir: pathlib.Path) -> None:
    download("2020-01-01", "2020-01-01", "nemde", base_directory=base_dir)
    data = load(base_directory=base_dir)["nemde"]
    #  TODO could link back to constants - chooing not to
    assert data["interval-start"].dt.tz.zone == "Etc/GMT-10"

    download("2020-01", "2020-02", "trading-price", base_directory=base_dir)
    data = load(base_directory=base_dir)["trading-price"]
    #  TODO could link back to constants - chooing not to
    assert data["interval-start"].dt.tz.zone == "Etc/GMT-10"
