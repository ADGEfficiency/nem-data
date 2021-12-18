from nemdata.cli import download


def test_system():
    download("2020-01", "2020-02", "trading-price")
    download("2020-01-01", "2020-01-02", "nemde")

    #  could test data is in the right place
    #  but test is most useful just to see if it runs without error ^^
