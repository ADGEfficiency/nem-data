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


def test_loader_dispatch_prices(base_dir: pathlib.Path) -> None:
    download("2019-01", "2019-02", "dispatch-price", base_directory=base_dir)
    data = load(base_directory=base_dir)["dispatch-price"]
    assert data["interval-start"].min() == pd.Timestamp("2019-01-01T00:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-02-28T23:55:00+1000")
    data = load(desired_reports=["dispatch-price"], base_directory=base_dir)[
        "dispatch-price"
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
    assert data["interval-start"].min() == pd.Timestamp("2019-07-02T04:00:00+1000")
    assert data["interval-start"].max() == pd.Timestamp("2019-07-06T03:55:00+1000")

    #  TODO
    # data = load(base_directory=base_dir, start="2019-07-03", end="2019-07-04")["nemde"]
    # assert data["interval-start"].min() == pd.Timestamp("2019-07-03T00:00:00+1000")
    # assert data["interval-start"].max() == pd.Timestamp("2019-08-04T23:55:00+1000")


def test_loader_predispatch(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-01", "predispatch", base_directory=base_dir)
    data = load(base_directory=base_dir)["predispatch"]
    assert data["interval-start"].min() == pd.Timestamp('2020-01-01 04:00:00+1000', tz='Etc/GMT-10')
    assert data["interval-start"].max() == pd.Timestamp('2020-02-02 03:30:00+1000', tz='Etc/GMT-10')


def test_loader_p5min(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-01", "p5min", base_directory=base_dir)
    data = load(base_directory=base_dir)["p5min"]
    assert data["interval-start"].min() == pd.Timestamp('2020-01-01 00:00:00+1000', tz='Etc/GMT-10')
    assert data["interval-start"].max() == pd.Timestamp('2020-02-01 00:50:00+1000', tz='Etc/GMT-10')


def test_loader_predispatch_sensitivities(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-01", "predispatch-sensitivities", base_directory=base_dir)
    data = load(base_directory=base_dir)["predispatch-sensitivities"]
    assert data["interval-start"].min() == pd.Timestamp('2020-01-01 04:00:00+1000', tz='Etc/GMT-10')
    assert data["interval-start"].max() == pd.Timestamp('2020-02-01 03:30:00+1000', tz='Etc/GMT-10')


def test_loader_predispatch_demand(base_dir: pathlib.Path) -> None:
    download("2020-01", "2020-01", "predispatch-demand", base_directory=base_dir)
    data = load(base_directory=base_dir)["predispatch-demand"]
    assert data["interval-start"].min() == pd.Timestamp('2020-01-01 04:00:00+1000', tz='Etc/GMT-10')
    assert data["interval-start"].max() == pd.Timestamp('2020-02-02 03:30:00+1000', tz='Etc/GMT-10')

