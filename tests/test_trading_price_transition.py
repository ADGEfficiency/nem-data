
    data = download_mmsdm(start="2021-09", end="2021-09", table_name="trading-price")
    assert all(data['frequency_minutes'] == 30)
    data = download_mmsdm(start="2021-10", end="2021-10", table_name="trading-price")
    assert all(data['frequency_minutes'] == 5)
    data = download_mmsdm(start="2021-11", end="2021-11", table_name="trading-price")
    assert all(data['frequency_minutes'] == 5)
