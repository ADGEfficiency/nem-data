import zipfile
from pathlib import Path
from nemdata import models as m
from typing import List


def unzip(path: Path):
    try:
        with zipfile.ZipFile(path, "r") as zip_ref:
            zip_ref.extractall(path.parent)
    except:
        print(f"failed unzip {path}")


def load_unzipped_report(raw_fi, skiprows=1, tail=-1):
    #  remove first row via skiprows
    data = pd.read_csv(raw_fi, skiprows=skiprows)
    #  remove last row via iloc
    return data.iloc[:tail, :]


def convert_datetime_columns(data, dt_cols):
    dt_cols += ["interval-start", "interval-end", "timestamp"]
    for col in dt_cols:
        try:
            data[col] = pd.to_datetime(data[col])
        except KeyError:
            pass
    return data


def add_interval_columns(data, timestamp_col, freq):
    """assuming timestamp_col is interval end"""
    interval = data[timestamp_col]
    data.loc[:, "interval-end"] = interval
    data.loc[:, "interval-start"] = interval - pd.Timedelta(freq)
    return data


def process_raw_data(unit: m.UOW):

    #  unzip the CSV from the raw zip downloaded earlier
    unzip(unit.raw_fi)

    #  read zip - removing first & last rows
    data = load_unzipped_report(unit.raw_fi)

    #  make datetime columns
    data = convert_datetime_columns(data, table.dt_cols)

    #  add_interval cols
    data = add_interval_columns(data, table.timestamp_column, table.freq)

    #  save clean.csv & clean.parquet
    data.to_csv(unit.processed_fi.with_suffix(".csv"))
    data.to_parquet(unit.processed_fi.with_suffix(".parquet"))


def process_raw_datas(datas: List[m.UOW]):
    import multiprocessing

    with multiprocessing.Pool(8) as pool:
        pool.map(process_raw_data, datas)
