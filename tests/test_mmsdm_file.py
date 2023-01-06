import pathlib

import pytest

from nemdata import mmsdm


@pytest.mark.parametrize(
    "year, month, table, name, expected",
    [
        (
            2019,
            1,
            "DISPATCHINTERCONNECTORRES",
            "interconnectors",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_01/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201901010000.zip",
        ),
        (
            2019,
            2,
            "FAKEREPORT",
            "fake",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_02/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_FAKEREPORT_201902010000.zip",
        ),
        (
            2010,
            12,
            "DISPATCHINTERCONNECTORRES",
            "interconnectors",
            "https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2010/MMSDM_2010_12/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201012010000.zip",
        ),
    ],
)
def test_form_report_url(
    year: int, month: int, table: str, name: str, expected: str, base_dir: pathlib.Path
) -> None:
    mmsdm_table = mmsdm.MMSDMTable(
        name=name,
        table=table,
        directory="DATA",
    )
    file = mmsdm.make_one_mmsdm_file(
        year, month=month, table=mmsdm_table, base_directory=base_dir
    )
    assert file.url == expected
