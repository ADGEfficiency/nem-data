import pathlib
import typing

import pandas as pd
from rich import print

from nemdata.config import DEFAULT_BASE_DIR


def concat(report_id: pathlib.Path, pkg: dict) -> dict:
    data = [p for p in report_id.glob("**/clean.parquet")]
    data = [pd.read_parquet(p) for p in data]
    pkg[report_id.name] = pd.concat(data, axis=0)
    return pkg


def concat_trading_price(report_id: pathlib.Path, pkg: dict) -> dict:
    fis = [p for p in report_id.glob("**/clean.parquet")]
    datas = []
    for fi in fis:
        data = pd.read_parquet(fi)
        for region in data["REGIONID"].unique():
            raw = data[data["REGIONID"] == region]
            raw = raw.set_index("interval-start").sort_index()

            if pd.infer_freq(raw.index) == "30T":
                #  need to add on a period to get what we want after resample
                raw.loc[raw.index[-1] + pd.Timedelta("25T"), :] = raw.iloc[-1, :]
            subset = raw.resample("5T").ffill()
            subset["interval-end"] = subset.index + pd.Timedelta("5T")
            datas.append(subset)

    pkg[report_id.name] = pd.concat(datas).reset_index()
    return pkg


def loader(
    desired_reports: typing.Union[dict, None] = None,
    *,
    base_dir: pathlib.Path = DEFAULT_BASE_DIR,
) -> dict:
    pkg: dict = {}
    base_dir = pathlib.Path(base_dir)
    report_ids = [p for p in base_dir.iterdir() if p.is_dir()]
    print(f" found {[r.name for r in report_ids]}")

    #  default to loading everything
    if desired_reports is not None:
        report_ids = [p for p in report_ids if p.name in desired_reports]

    print(f"[bold green]Loader[/]: {[r.name for r in report_ids]}")

    for report_id in report_ids:
        if report_id.name == "trading-price":
            pkg = concat_trading_price(report_id, pkg)
        else:
            pkg = concat(report_id, pkg)

    return pkg
