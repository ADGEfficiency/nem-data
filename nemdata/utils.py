from collections import namedtuple

import pandas as pd
import requests
from rich import print

URL = namedtuple("url", "url, year, month, report, csv, xml, home")


def download_zipfile_from_url(url, chunk_size=128):
    path = url.home / "raw.zip"
    print(f" [green]downloading[/] {path.parts[-5:]}")
    r = requests.get(url.url, stream=True)
    with open(path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
    return path


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
