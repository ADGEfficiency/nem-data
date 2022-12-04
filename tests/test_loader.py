import pandas as pd
import pytest

from nemdata.cli import download
from nemdata.loader import loader


@pytest.fixture(scope="function")
def base_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("nem-data") / "data"


def test_loader_unit_scada(base_dir):
    download("2020-01", "2020-02", "unit-scada", base_dir=base_dir)
    data = loader(base_dir=base_dir)["unit-scada"]
    assert data["interval-start"].min() == pd.Timestamp("2020-01-01T00:00:00")
    assert data["interval-start"].max() == pd.Timestamp("2020-02-29T23:55:00")


def test_loader_trading_prices(base_dir):
    download("2019-01", "2019-02", "trading-price", base_dir=base_dir)
    data = loader(base_dir=base_dir)["trading-price"]
    assert data["interval-start"].min() == pd.Timestamp("2019-01-01T00:00:00")
    assert data["interval-start"].max() == pd.Timestamp("2019-02-28T23:55:00")


def test_loader_trading_prices_leap_year(base_dir):
    download("2020-01", "2020-02", "trading-price", base_dir=base_dir)
    data = loader(base_dir=base_dir)["trading-price"]
    assert data["interval-start"].min() == pd.Timestamp("2020-01-01T00:00:00")
    assert data["interval-start"].max() == pd.Timestamp("2020-02-29T23:55:00")
