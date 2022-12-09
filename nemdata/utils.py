import pathlib
import typing
from collections import namedtuple

import pandas as pd
import requests
from rich import print

import nemdata

URL = namedtuple("url", "url, year, month, report, csv, xml, home")


headers = {
    "referer": "https://aemo.com.au/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}


def download_zipfile(
    file: "typing.Union[nemdata.mmsdm.MMSDMFile, nemdata.nemde.NEMDEFile]",
    chunk_size: int = 128,
) -> None:
    """download zipfile from a url and write to `file.data_directory / raw.zip`"""
    request = requests.get(file.url, stream=True, headers=headers)
    assert request.ok
    with open(file.zipfile_path, "wb") as fd:
        for chunk in request.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def unzip(path):
    import zipfile

    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(path.parent)


def add_interval_cols(data, timestamp_col, freq):
    """assuming timestamp_col is interval end"""
    interval = data[timestamp_col]
    data.loc[:, "interval-end"] = interval
    data.loc[:, "interval-start"] = interval - pd.Timedelta(freq)
    return data
