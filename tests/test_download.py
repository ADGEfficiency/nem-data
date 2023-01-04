import pathlib

from _pytest.capture import CaptureFixture

from nemdata.downloader import download


def test_system_mmsdm(base_dir: pathlib.Path, capsys: CaptureFixture) -> None:
    months = ["2020-01", "2020-02"]
    for month in months:
        assert not (base_dir / "trading-price" / month / "clean.parquet").exists()
        download(start=month, end=month, table="trading-price", base_directory=base_dir)
        assert (base_dir / "trading-price" / month / "clean.parquet").exists()

    capsys.readouterr()
    repeat_months = ["2020-02"]
    for month in repeat_months:
        download(start=month, end=month, table="trading-price", base_directory=base_dir)
        assert (base_dir / "trading-price" / month / "clean.parquet").exists()
        captured = capsys.readouterr()
        assert "CACHED" in captured.out
        assert not "NOT CACHED" in captured.out


def test_system_nemde(base_dir: pathlib.Path, capsys: CaptureFixture) -> None:
    days = ["2020-01-01", "2020-01-02"]
    for day in days:
        assert not (base_dir / "nemde" / day / "clean.parquet").exists()
        download(start=day, end=day, table="nemde", base_directory=base_dir)
        assert (base_dir / "nemde" / day / "clean.parquet").exists()

    capsys.readouterr()
    repeat_days = ["2020-01-02"]
    for day in repeat_days:
        download(start=day, end=day, table="nemde", base_directory=base_dir)
        assert (base_dir / "nemde" / day / "clean.parquet").exists()
        captured = capsys.readouterr()
        assert "CACHED" in captured.out
        assert not "NOT CACHED" in captured.out
