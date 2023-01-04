import pathlib
import typing
import warnings
import zipfile

import numpy as np
import pandas as pd
import requests

from nemdata import mmsdm, nemde

headers = {
    "referer": "https://aemo.com.au/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
}


def download_zipfile(
    file: "typing.Union[mmsdm.MMSDMFile, nemde.NEMDEFile]",
    chunk_size: int = 128,
) -> bool:
    """download zipfile from a url and write to `file.data_directory / raw.zip`"""
    request = requests.get(file.url, stream=True, headers=headers)
    is_data_available = request.ok
    if is_data_available:
        with open(file.zipfile_path, "wb") as fd:
            for chunk in request.iter_content(chunk_size=chunk_size):
                fd.write(chunk)

    return is_data_available


def unzip(path: pathlib.Path) -> None:
    """unzip a zip file to it's parent path"""
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall(path.parent)


def add_interval_column(
    data: pd.DataFrame,
    table: "typing.Union[mmsdm.MMSDMTable, nemde.NEMDETable]",
) -> pd.DataFrame:
    """add the `interval-start` and `interval-end` columns"""

    interval = data[table.interval_column]
    data.loc[:, "interval-end"] = interval

    if isinstance(table.frequency, int):
        data.loc[:, "frequency_minutes"] = table.frequency
    else:
        assert table.frequency
        before_transition = (
            data.loc[:, "interval-end"]
            < table.frequency.transition_datetime_interval_end
        )
        data.loc[
            before_transition, "frequency_minutes"
        ] = table.frequency.frequency_minutes_before

        after_transition = (
            data.loc[:, "interval-end"]
            >= table.frequency.transition_datetime_interval_end
        )
        data.loc[
            after_transition, "frequency_minutes"
        ] = table.frequency.frequency_minutes_after

    #  ignore performance warning about no vectorization
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
        data.loc[:, "interval-start"] = interval - np.array(
            [pd.Timedelta(minutes=int(f)) for f in data["frequency_minutes"].values]
        )
    return data
