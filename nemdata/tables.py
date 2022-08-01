from typing import Union
from nemdata import models as m
from nemdata.database import homebase

import pandas as pd
from datetime import date
import pandas as pd
from rich import print

from typing import List


prefix = f"https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity"


class Table:
    database = None
    directory = None

    name = None
    table = None
    dt_cols = None
    timestamp_col = None
    freq = None


class NEMDE(Table):
    database = "NEMDE"
    directory = "NEMDE_Market_Data/NEMDE_Files"

    name = "nemde"
    table = "NemPriceSetter"
    dt_cols = ["PeriodID"]
    timestamp_col = "PeriodID"
    freq = "5T"

    def uow(self, year: int, month: int, day: int) -> "UOW":
        month = str(month).zfill(2)
        day = str(day).zfill(2)

        url_base = f"{prefix}/{self.database}/{year}/{self.database}_{year}_{month}/{self.directory}"
        fi = f"{self.table}_{year}{month}{day}"
        url = f"{url_base}/{fi}_xml.zip"
        xml = f"{fi}.xml"

        raw_zip = homebase / self.name / f"{year}-{month}-{day}" / "raw.zip"
        raw_zip.parent.mkdir(exist_ok=True, parents=True)
        raw_fi = raw_zip.parent / xml
        processed_fi = homebase / self.name / f"{year}-{month}-{day}" / "clean.parquet"

        return m.UOW(
            url=url,
            year=year,
            month=month,
            fi=xml,
            name=self.name,
            raw_fi=raw_fi,
            raw_zip=raw_zip,
            processed_fi=processed_fi,
            table=self.name,
        )

    def create_urls(self, start: date, end: date) -> List["UOW"]:
        days = pd.date_range(start=start, end=end, freq="D")
        urls = []
        for year, month, day in zip(days.year, days.month, days.day):
            urls.append(self.uow(year, month, day))

        print(f"created [green]{len(urls)} urls[/] for [blue]{self.name}[/] table")
        return urls

    def load_unzipped_data(self, raw_fi):
        from pathlib import Path

        path = raw_fi.parent
        fis = [p for p in Path(path).iterdir() if p.suffix == ".xml"]
        #  get problems with a value of '5' without the cast to float
        data = pd.concat([pd.read_xml(f) for f in fis], axis=0)
        data["BandNo"] = data["BandNo"].astype(float)
        return data


class MMSDM(Table):
    database = "MMSDM"
    directory = "MMSDM_Historical_Data_SQLLoader/DATA"

    def uow(self, year: int, month: int) -> "UOW":
        month = str(month).zfill(2)
        url_base = f"{prefix}/{self.database}/{year}/{self.database}_{year}_{month}/{self.directory}"

        fi = f"PUBLIC_DVD_{self.table}_{year}{month}010000"
        csv = f"{fi}.CSV"
        url = f"{url_base}/{fi}.zip"

        raw_zip = homebase / self.name / f"{year}-{month}" / "raw.zip"
        raw_zip.parent.mkdir(exist_ok=True, parents=True)
        raw_fi = raw_zip.parent / csv
        processed_fi = homebase / self.name / f"{year}-{month}" / "clean.parquet"

        return m.UOW(
            url=url,
            year=year,
            month=month,
            fi=csv,
            name=self.name,
            raw_zip=raw_zip,
            raw_fi=raw_fi,
            processed_fi=processed_fi,
            table=self.name,
        )

    def create_urls(self, start: date, end: date) -> List["UOW"]:
        months = pd.date_range(start=start, end=end, freq="MS")
        urls = []
        for year, month in zip(months.year, months.month):
            urls.append(self.uow(year, month))
        return urls

        print(f"created [green]{len(urls)} urls[/] for [blue]{self.name}[/] table")
        return urls

    def load_unzipped_data(self, raw_fi, skiprows=1, tail=-1):
        #  remove first row via skiprows
        data = pd.read_csv(raw_fi, skiprows=skiprows)
        #  remove last row via iloc
        return data.iloc[:tail, :]


class TradingPrice(MMSDM):
    name = "trading-price"
    table = "TRADINGPRICE"
    dt_cols = ["SETTLEMENTDATE"]
    timestamp_col = "SETTLEMENTDATE"
    freq = "30T/5T"


class PredispatchPrice(MMSDM):
    name = "predispatch-price"
    table = "PREDISP_ALL_DATA"
    dt_cols = ["LASTCHANGED", "DATETIME"]
    timestamp_col = "DATETIME"
    freq = "30T/5T"


tables = {"nemde": NEMDE(), "trading-price": TradingPrice()}


def get_table(table: str) -> Union[NEMDE, MMSDM]:
    return tables[table]
