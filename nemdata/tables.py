from typing import Union
from nemdata import models as m
from nemdata.database import homebase


prefix = f"https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity"


class NEMDE:
    def url(self, year: int, month: int):
        pass


class MMSDM:
    database = "MMSDM"
    directory = "DATA"
    name = None

    def uow(self, year: int, month: int) -> "UOW":
        #  zero pad the month
        month = str(month).zfill(2)

        url_base = f"{prefix}/{self.database}/{year}/MMSDM_{year}_{month}/MMSDM_Historical_Data_SQLLoader/{self.directory}"
        fi = f"PUBLIC_DVD_{self.table}_{year}{month}010000"
        csv = f"{fi}.CSV"
        url = f"{url_base}/{fi}.zip"

        raw_fi = homebase / self.name / f"{year}-{month}" / "raw.zip"
        raw_fi.parent.mkdir(exist_ok=True, parents=True)

        processed_fi = homebase / self.name / f"{year}-{month}" / "clean.parquet"

        return m.UOW(
            url=url, year=year, month=month, csv=csv, name=self.name, raw_fi=raw_fi
        )


class TradingPrice(MMSDM):
    name = "trading-price"
    table = "TRADINGPRICE"


tables = {"nemde": NEMDE(), "trading-price": TradingPrice()}


def get_table(table: str) -> Union[NEMDE, MMSDM]:
    return tables[table]
