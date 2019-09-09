import pytest

from nemdata.use_cases import form_report_url


# @pytest.mark.parametrize(
#     'year, month, expected',
#     [
#         (2018, 1, 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2018/MMSDM_2018_01.zip'),
#         (2018, 1, 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2018/MMSDM_2018_01.zip'),
#         (2012, 12, 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2012/MMSDM_2012_12.zip')
#     ]
# )
# def test_form_mmsdm_url(year, month, expected):
#     url = form_mmsdm_url(year, month)
#     assert url == expected


@pytest.mark.parametrize(
    'year, month, report, expected',
    [
        (2019, 1, 'DISPATCHINTERCONNECTORRES', 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_01/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201901010000.zip'),
        (2019, 2, 'DISPATCHINTERCONNECTORRES', 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2019/MMSDM_2019_02/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201902010000.zip'),
        (2010, 12, 'DISPATCHINTERCONNECTORRES', 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2010/MMSDM_2010_12/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_DISPATCHINTERCONNECTORRES_201012010000.zip')
    ]
)
def test_form_report_url(year, month, report, expected):
    url = form_report_url(year, month, report)
    assert url == expected
