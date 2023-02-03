import pathlib

import pandas as pd

from nemdata.cli import download
from nemdata.loader import load


def test_loader_unit_scada(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-01", "unit-scada", base_directory=base_dir)
    data = load(base_directory=base_dir)["unit-scada"]
    assert data["interval-start"].min() == pd.Timestamp("2020-01-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2020-01-31T23:55:00+1000")


def test_loader_trading_prices(base_dir: pathlib.Path) -> None:
    download("2019-01", "2019-02", "trading-price", base_directory=base_dir)
    data = load(base_directory=base_dir)["trading-price"]
    assert data["interval-start"].min() == pd.Timestamp("2019-01-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-02-28T23:55:00+1000")
    data = load(desired_reports=["trading-price"], base_directory=base_dir)[
        "trading-price"
    ]


def test_loader_trading_prices_leap_year(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-02", "trading-price", base_directory=base_dir)
    data = load(base_directory=base_dir)["trading-price"]
    assert data["interval-start"].min() == pd.Timestamp("2020-01-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2020-02-29T23:55:00+1000")


def test_loader_demand(base_dir: pathlib.Path) -> None:
    download("2020-04", "2020-05", "demand", base_directory=base_dir)
    data = load(base_directory=base_dir)["demand"]
    assert data["interval-start"].min() == pd.Timestamp("2020-04-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2020-05-31T23:55:00+1000")


def test_loader_interconnectors(base_dir: pathlib.Path) -> None:
    download("2019-07", "2019-08", "interconnectors", base_directory=base_dir)
    data = load(base_directory=base_dir)["interconnectors"]
    assert data["interval-start"].min() == pd.Timestamp("2019-07-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-08-31T23:55:00+1000")


def test_loader_nemde(base_dir: pathlib.Path) -> None:
    download("2019-07-02", "2019-07-05", "nemde", base_directory=base_dir)
    data = load(base_directory=base_dir)["nemde"]
    assert data["interval-start"].min() == pd.Timestamp("2019-07-02T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-08-05T23:55:00+1000")

    data = load(base_directory=base_dir, start="2019-07-03", end="2019-07-04")["nemde"]
    assert data["interval-start"].min() == pd.Timestamp("2019-07-03T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-08-04T23:55:00+1000")
