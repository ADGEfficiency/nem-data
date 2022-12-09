import pathlib

from nemdata.mmsdm import download_mmsdm


def test_trading_price_transition(base_dir: pathlib.Path) -> None:
    data = download_mmsdm(
        start="2021-09",
        end="2021-09",
        table_name="trading-price",
        base_directory=base_dir,
    )
    assert all(data["frequency_minutes"] == 30)
    data = download_mmsdm(
        start="2021-10",
        end="2021-10",
        table_name="trading-price",
        base_directory=base_dir,
    )
    assert all(data["frequency_minutes"] == 5)
    data = download_mmsdm(
        start="2021-11",
        end="2021-11",
        table_name="trading-price",
        base_directory=base_dir,
    )
    assert all(data["frequency_minutes"] == 5)
