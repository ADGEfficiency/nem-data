from nemdata.cli import cli


def test_system():
    cli("2020-01", "2020-02", "trading-price")
    cli("2020-01-01", "2020-01-02", "nemde", use_async=True, use_multiprocess=True)
