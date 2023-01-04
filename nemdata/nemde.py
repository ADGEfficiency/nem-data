import datetime
import pathlib
import typing
import warnings

import numpy as np
import pandas as pd
import pydantic
import requests
from rich import print

from nemdata import utils
from nemdata.config import DEFAULT_BASE_DIRECTORY
from nemdata.constants import constants


class NEMDETable(pydantic.BaseModel):
    frequency: int = 5
    interval_column: str = "PeriodID"


class NEMDEFile(pydantic.BaseModel):
    year: int
    month: int
    day: int
    url: str
    xml_name: str
    data_directory: pathlib.Path
    zipfile_path: pathlib.Path


def make_many_nemde_files(
    start: str, end: str, base_directory: pathlib.Path
) -> list[NEMDEFile]:
    """creates many NEMDEFiles - one for each day"""

    files = []
    months = pd.date_range(start=start, end=end, freq="D")
    for year, month, day in zip(months.year, months.month, months.day):
        files.append(
            make_one_nemde_file(
                year=year, month=month, day=day, base_directory=base_directory
            )
        )
    return files


def make_one_nemde_file(
    year: int, month: int, day: int, base_directory: pathlib.Path
) -> NEMDEFile:

    padded_month = str(month).zfill(2)
    padded_day = str(day).zfill(2)

    url = f"http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/{year}/NEMDE_{year}_{padded_month}/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_{year}{padded_month}{padded_day}_xml.zip"

    xml_name = f"NemPriceSetter_{year}{padded_month}{padded_day}.xml"

    data_directory = base_directory / "nemde" / f"{year}-{padded_month}-{padded_day}"
    data_directory.mkdir(exist_ok=True, parents=True)

    return NEMDEFile(
        year=year,
        month=month,
        day=day,
        url=url,
        xml_name=xml_name,
        data_directory=data_directory,
        zipfile_path=data_directory / "raw.zip",
    )


def find_xmls(path: pathlib.Path) -> list[pd.DataFrame]:
    """find all XML files in a directory"""
    fis = [p for p in path.iterdir() if p.suffix == ".xml"]
    return [pd.read_xml(f) for f in fis]


def download_nemde(
    start: str,
    end: str,
    table_name: str = "nemde",
    base_directory: pathlib.Path = DEFAULT_BASE_DIRECTORY,
    dry_run: bool = False,
) -> pd.DataFrame:
    """main for downloading MMSDMFiles"""
    table = NEMDETable()
    files = make_many_nemde_files(start, end, base_directory)
    dataset = []
    for file in files:
        data = download_one_nemde(table, file, dry_run)

        if data is not None:
            dataset.append(data)

    try:
        return pd.concat(dataset, axis=0)
    except ValueError:
        return pd.DataFrame()


def download_one_nemde(
    table: NEMDETable, file: NEMDEFile, dry_run: bool
) -> typing.Union[pd.DataFrame, None]:
    clean_fi = file.data_directory / "clean.parquet"
    if clean_fi.exists():
        print(f" [blue]CACHED[/] {' '.join(clean_fi.parts[-5:])}")
        return pd.read_parquet(clean_fi)
    else:
        print(f" [blue]NOT CACHED[/] {' '.join(clean_fi.parts[-5:])}")

    data_available = utils.download_zipfile(file)

    if not data_available:
        print(f" [red]NOT AVAILABLE[/] {' '.join(file.zipfile_path.parts[-5:])}")
        return None

    else:
        print(f" [green]DOWNLOADING[/] {' '.join(file.zipfile_path.parts[-5:])}")
        utils.download_zipfile(file)
        utils.unzip(file.zipfile_path)
        xmls = find_xmls(file.data_directory)
        data = pd.concat(xmls, axis=0)

        #  get problems with a value of '5' without the cast to float
        data["BandNo"] = data["BandNo"].astype(float)

        #  already timezone aware here
        data["PeriodID"] = pd.to_datetime(data["PeriodID"])
        assert data["PeriodID"].dt.tz._offset == datetime.timedelta(seconds=3600 * 10)
        data["PeriodID"] = data["PeriodID"].dt.tz_convert(constants.nem_tz)
        data = utils.add_interval_column(data, table)

        if not dry_run:
            print(f" [green]SAVING [/] {clean_fi}")
            data.to_csv(clean_fi.with_suffix(".csv"))
            data.to_parquet(clean_fi.with_suffix(".parquet"))
        return data
