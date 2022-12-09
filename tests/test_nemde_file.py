import pytest

from nemdata import nemde
from nemdata.config import DEFAULT_BASE_DIR


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
    file = nemde.make_one_nemde_file(year, month, day, base_dir=DEFAULT_BASE_DIR)
    assert file.url == expected
