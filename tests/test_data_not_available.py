import pathlib

from nemdata.downloader import download
from nemdata.mmsdm import find_mmsdm_table, make_one_mmsdm_file
from nemdata.utils import download_zipfile


def test_data_not_available_integration(base_dir: pathlib.Path) -> None:
    data = download(
        start="1990-01", end="1990-01", table="trading-price", base_directory=base_dir
    )
    assert data.shape[0] == 0
    assert data.shape[1] == 0

    data = download(
        start="1990-01-01", end="1990-01-02", table="nemde", base_directory=base_dir
    )
    assert data.shape[0] == 0
    assert data.shape[1] == 0


def test_data_not_available(base_dir: pathlib.Path) -> None:
    table = find_mmsdm_table("trading-price")
    mmsdm_file = make_one_mmsdm_file(2020, 1, table, base_dir)
    assert download_zipfile(mmsdm_file)

    mmsdm_file = make_one_mmsdm_file(1990, 1, table, base_dir)
    assert not download_zipfile(mmsdm_file)
