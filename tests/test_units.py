import pytest

from nemdata.mmsdm import make_report_url
from nemdata.nemde import make_nemde_url


@pytest.mark.parametrize(
    "year, month, day, expected",
    [
        (
            2019,
            1,
            1,
            "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/2019/NEMDE_2019_01/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_20190101_xml.zip",
        ),
        (
            2018,
            11,
            31,
            "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/2018/NEMDE_2018_11/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_20181131_xml.zip",
        ),
        (
            2009,
            8,
            22,
            "http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/2009/NEMDE_2009_08/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_20090822_xml.zip",
        ),
    ],
)
def test_form_nemde_url(year, month, day, expected):
    url = make_nemde_url(year, month, day)
    assert url.url == expected


@pytest.mark.parametrize(
    "year, month, report, expected",
    [
        (
            2019,
            1,
            "DISPATCHINTERCONNECTORRES",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_01/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201901010000.zip",
        ),
        (
            2019,
            2,
            "FAKEREPORT",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_02/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_FAKEREPORT_201902010000.zip",
        ),
        (
            2010,
            12,
            "DISPATCHINTERCONNECTORRES",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2010/MMSDM_2010_12/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201012010000.zip",
        ),
    ],
)
def test_form_report_url(year, month, report, expected):
    url = make_report_url(year, month, report)
    assert url.url == expected
