import pathlib

import pytest

from nemdata import nemde


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
def test_form_nemde_url(
    year: int, month: int, day: int, expected: str, base_dir: pathlib.Path
) -> None:
    file = nemde.make_one_nemde_file(year, month, day, base_directory=base_dir)
    assert file.url == expected
