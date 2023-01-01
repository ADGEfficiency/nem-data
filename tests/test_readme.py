import pathlib


def test_readme(base_dir: pathlib.Path) -> None:
    import nemdata

    data = nemdata.download(
        start="2020-01", end="2020-02", table="trading-price", base_directory=base_dir
    )
    data = nemdata.load(base_directory=base_dir)["trading-price"]
