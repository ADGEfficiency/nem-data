from datetime import date
import pandas as pd
from rich import print

from typing import List


def create_urls(start: date, end: date, table) -> List["UOW"]:
    # return [
    #     'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2022/MMSDM_2022_06/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_TRADINGPRICE_202206010000.zip',
    #     'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/2022/MMSDM_2022_06/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_TRADINGPRICE_202207010000.zip'
    # ]
    months = pd.date_range(start=start, end=end, freq="MS")

    urls = []
    for year, month in zip(months.year, months.month):
        urls.append(table.uow(year, month))

    print(f" created [green]{len(urls)} urls[/] for [blue]{table.name}[/] table")
    return urls
