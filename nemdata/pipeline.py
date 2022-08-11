import zipfile
from pathlib import Path
from typing import List
import datetime
from rich import print
import multiprocessing

import pandas as pd

from nemdata import models as m
from nemdata.tables import get_table
from nemdata import cut_off


def unzip(path: Path):
    try:
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(path.parent)
    except:
        print(f"failed unzip {path}")


def convert_datetime_columns(data, dt_cols):
    dt_cols += ["interval-start", "interval-end", "timestamp"]
    for col in dt_cols:
        try:
            data[col] = pd.to_datetime(data[col])
        except KeyError:
            pass
    return data


def nem_settlement_change(dt):
    #  1/10/2021  12:05:00 AM
    if dt >= cut_off:
        return pd.Timedelta("5T")
    else:
        return pd.Timedelta("30T")


def add_interval_columns(data, freq, timestamp_col):
    #  deal with the timezone change
    #  create a vector of freqs based on that cutoff date

    if freq == "30T/5T":
        freq = data[timestamp_col].apply(nem_settlement_change)
    else:
        freq = pd.Timedelta(freq)

    interval = data[timestamp_col]
    data.loc[:, "interval-end"] = interval
    data.loc[:, "interval-start"] = interval - freq
    return data


def process_raw_data(uow: m.UOW):
    if uow.raw_fi.exists():
        table = get_table(uow.table)

        #  unzip the CSV from the raw zip downloaded earlier
        unzip(uow.raw_zip)

        #  read csv - removing first & last rows
        data = table.load_unzipped_data(uow.raw_fi)

        #  make datetime columns
        data = convert_datetime_columns(data, table.dt_cols)

        #  add_interval cols
        data = add_interval_columns(data, table.freq, table.timestamp_col)

        #  save clean.csv & clean.parquet
        data.to_csv(uow.processed_fi.with_suffix(".csv"))
        data.to_parquet(uow.processed_fi.with_suffix(".parquet"))
        print(f" [green]SUCCESS PROCESSED[/] {uow.processed_fi}")
        return "success"
    else:
        print(f" [red]FAIL PROCESSED[/] {uow.processed_fi}")
        return "fail"


def process_raw_datas(datas: List[m.UOW]):
    with multiprocessing.Pool(8) as pool:
        results = pool.map(process_raw_data, datas)

    successes = len(list(filter(lambda x: x == "success", results)))
    print(f"[green]PROCESSED[/] [blue]{successes}/{len(datas)} files[/]")
