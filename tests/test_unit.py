from nemdata import tables


def test_predispatch_url():
    table = tables.PredispatchPrice()
    work = table.create_uows("2022-06-01", "2022-07-01")[0]
    expected = "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2022/MMSDM_2022_06/MMSDM_Historical_Data_SQLLoader/PREDISP_ALL_DATA/PUBLIC_DVD_PREDISPATCHPRICE_202206010000.zip"
    assert work.url == expected


def test_trading_price_url():
    table = tables.TradingPrice()
    work = table.create_uows("2022-06-01", "2022-07-01")[0]
    expected = "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2022/MMSDM_2022_06/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_TRADINGPRICE_202206010000.zip"
    assert work.url == expected


def test_nemde_url():
    table = tables.NEMDE()
    work = table.create_uows("2022-06-01", "2022-07-01")[0]
    expected = "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/2022/NEMDE_2022_06/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_20220601_xml.zip"
    assert work.url == expected
