import pytest

from nemdata.config import DEFAULT_BASE_DIR
from nemdata import mmsdm_neu


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
def test_form_report_url(year, month, table, name, expected):
    table = mmsdm_neu.MMSDMTable(
        name=name,
        table=table,
        directory="DATA",
    )
    file = mmsdm_neu.make_one_mmsdm_file(
        year, month, table, base_directory=DEFAULT_BASE_DIR
    )
    assert file.url == expected
