from pathlib import Path

import pandas as pd

from nemdata.config import HOME
from nemdata.utils import download_zipfile_from_url, URL, unzip, add_interval_cols


reports = {
    "predispatch": {
        "report": "PREDISPATCHPRICE",
        "directory": "PREDISP_ALL_DATA",
        "dt-cols": ["LASTCHANGED", "DATETIME"],
        "interval-col": "DATETIME",
        "freq": "30T",
    },
    "unit-scada": {"report": "DISPATCH_UNIT_SCADA", "directory": "DATA"},
    "trading-price": {
        "report": "TRADINGPRICE",
        "directory": "DATA",
        "dt-cols": ["SETTLEMENTDATE"],
        "interval-col": "SETTLEMENTDATE",
        "freq": "30T",
    },
}


def make_report_url(year, month, report, directory):
    #  zero pad the month
    month = str(month).zfill(2)
    prefix = f"https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{year}/MMSDM_{year}_{month}/MMSDM_Historical_Data_SQLLoader"

    home = HOME / report / f"{year}-{month}"
    home.mkdir(exist_ok=True, parents=True)

    return URL(
        # url=f"{prefix}/{directory}/PUBLIC_DVD_{report}_{year}{month}010000.zip",
        url=f"{prefix}/{directory}/PUBLIC_DVD_{report}_{year}{month}010000.zip",
        year=year,
        month=month,
        report=report,
        csv=f"PUBLIC_DVD_{report}_{year}{month}010000.CSV",
        xml=None,
        home=home,
    )


def make_many_report_urls(start, end, report_id):
    report = reports[report_id]
    months = pd.date_range(start=start, end=end, freq="MS")

    urls = []
    for year, month in zip(months.year, months.month):
        urls.append(make_report_url(year, month, report["report"], report["directory"]))
    return urls


def load_unzipped_report(url, path, skiprows=1, tail=-1):
    path = path.parent / url.csv
    #  remove first row via skiprows
    data = pd.read_csv(path, skiprows=skiprows)
    #  remove last row via iloc
    return data.iloc[:tail, :]


def make_dt_cols(data, dt_cols):
    dt_cols += ["interval-start", "interval-end", "timestamp"]
    for col in dt_cols:
        try:
            data[col] = pd.to_datetime(data[col])
        except KeyError:
            pass
    return data


def download_mmsdm(start, end, report_id):
    urls = make_many_report_urls(start, end, report_id)

    output = []
    for url in urls:
        zf = download_zipfile_from_url(url)
        unzip(zf)

        data = load_unzipped_report(url, zf)

        #  unpacking the report dict - must be better way...
        report = reports[report_id]
        timestamp_col = report["interval-col"]

        data = make_dt_cols(data, report["dt-cols"])

        #  accounting for AEMO stamping intervals at the end
        #  usually intervals are stamped at the start

        freq = report["freq"]
        interval_col = report["interval-col"]
        data = add_interval_cols(data, timestamp_col, freq)

        #  could check by assert difference == freq
        path = Path(zf.parent)
        print(f" saving csv and parquet to {path}/clean")
        data.to_csv(path / "clean.csv")
        data.to_parquet(path / "clean.parquet")

        output.append(data)

    return pd.concat(output, axis=0)
