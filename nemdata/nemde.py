import datetime
import pathlib
import typing
import warnings

import numpy as np
import pandas as pd
import pydantic
import requests
from rich import print

import nemdata
from nemdata import utils
from nemdata.config import DEFAULT_BASE_DIRECTORY


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


def find_xmls(path):
    fis = [p for p in path.iterdir() if p.suffix == ".xml"]
    return [pd.read_xml(f) for f in fis]


def download_nemde(
    start: str,
    end: str,
    base_directory: pathlib.Path = DEFAULT_BASE_DIRECTORY,
):
    """main for downloading MMSDMFiles"""
    files = make_many_nemde_files(start, end, base_directory)
    dataset = []
    for file in files:
        clean_fi = file.data_directory / "clean.parquet"
        if clean_fi.exists():
            print(f" [blue]EXISTS[/] {' '.join(clean_fi.parts[-5:])}")
            data = pd.read_parquet(clean_fi)
        else:
            print(f" [blue]MISSING[/] {' '.join(clean_fi.parts[-5:])}")
            print(f" [green]DOWNLOADING[/] {' '.join(file.zipfile_path.parts[-5:])}")
            utils.download_zipfile(file)
            utils.unzip(file.zipfile_path)
            xmls = find_xmls(file.data_directory)
            data = pd.concat(xmls, axis=0)
            #  get problems with a value of '5' without the cast to float
            data["BandNo"] = data["BandNo"].astype(float)

            #  accounting for AEMO stamping intervals at the end
            #  usually intervals are stamped at the start
            data["PeriodID"] = pd.to_datetime(data["PeriodID"]).dt.tz_localize(None)
            data = utils.add_interval_cols(data, "PeriodID", "5T")

            print(f" [green]SAVING [/] {clean_fi}")
            data.to_csv(clean_fi.with_suffix(".csv"))
            data.to_parquet(clean_fi.with_suffix(".parquet"))
        dataset.append(data)
    return pd.concat(dataset, axis=0)


if __name__ == "__main__":
    download_nemde(start="2021-10-01", end="2021-10-01")
