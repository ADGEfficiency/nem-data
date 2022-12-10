import pathlib

from nemdata.cli import download


def test_system_mmsdm(base_dir: pathlib.Path) -> None:
    months = ["2020-01", "2020-02"]
    for month in months:
        assert not (base_dir / "trading-price" / month / "clean.parquet").exists()
        download(
            start=month, end=month, table_name="trading-price", base_directory=base_dir
        )
        assert (base_dir / "trading-price" / month / "clean.parquet").exists()


def test_system_nemde(base_dir: pathlib.Path) -> None:
    days = ["2020-01-01", "2020-01-02"]
    for day in days:
        assert not (base_dir / "nemde" / day / "clean.parquet").exists()
        download(start=day, end=day, table_name="nemde", base_directory=base_dir)
        assert (base_dir / "nemde" / day / "clean.parquet").exists()
