from nemdata.cli import download
from nemdata.loader import loader
import pandas as pd


def test_loader_unit_scada():
    download("2020-01", "2020-02", "unit-scada")
    data = loader()['unit-scada']
    assert data['interval-start'].min() == pd.Timestamp("2020-01-01T00:00:00")
    assert data['interval-start'].max() == pd.Timestamp("2020-02-29T23:55:00")
