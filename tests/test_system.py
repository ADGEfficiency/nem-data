from nemdata.cli import download


def test_system(tmp_path_factory):
    base_dir = tmp_path_factory.mktemp("nem-data") / "data"

    months = ["2020-01", "2020-02"]
    for month in months:
        assert not (base_dir / "trading-price" / month / "clean.parquet").exists()
    download(*months, "trading-price", base_dir=base_dir)

    for month in months:
        assert (base_dir / "trading-price" / month / "clean.parquet").exists()

    days = ["2020-01-01", "2020-01-02"]
    for day in days:
        assert not (base_dir / "nemde" / day / "clean.parquet").exists()
    download(*days, "nemde", base_dir=base_dir)

    for day in days:
        assert (base_dir / "nemde" / day / "clean.parquet").exists()
