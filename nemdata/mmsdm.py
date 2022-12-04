from pathlib import Path

import pandas as pd
from rich import print

from nemdata.utils import URL, add_interval_cols, download_zipfile_from_url, unzip

reports = {
    "predispatch": {
        "report": "PREDISPATCHPRICE",
        "directory": "PREDISP_ALL_DATA",
        "dt-cols": ["LASTCHANGED", "DATETIME"],
        "interval-col": "DATETIME",
        "freq": "30T",
    },
    "unit-scada": {
        "report": "DISPATCH_UNIT_SCADA",
        "directory": "DATA",
        "interval-col": "SETTLEMENTDATE",
        "dt-cols": ["SETTLEMENTDATE"],
        "freq": "5T",
    },
    "trading-price": {
        "report": "TRADINGPRICE",
        "directory": "DATA",
        "dt-cols": ["SETTLEMENTDATE"],
        "interval-col": "SETTLEMENTDATE",
        "freq": "30T",
    },
}


def make_report_url(year, month, report, directory, report_id, base_dir):
    #  zero pad the month
    month = str(month).zfill(2)
    prefix = f"https://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{year}/MMSDM_{year}_{month}/MMSDM_Historical_Data_SQLLoader"

    home = base_dir / report_id / f"{year}-{month}"
    home.mkdir(exist_ok=True, parents=True)

    return URL(
        url=f"{prefix}/{directory}/PUBLIC_DVD_{report}_{year}{month}010000.zip",
        year=year,
        month=month,
        report=report,
        csv=f"PUBLIC_DVD_{report}_{year}{month}010000.CSV",
        xml=None,
        home=home,
    )


def make_many_report_urls(start, end, report_id, base_dir):
    report = reports[report_id]
    months = pd.date_range(start=start, end=end, freq="MS")

    urls = []
    for year, month in zip(months.year, months.month):
        urls.append(
            make_report_url(
                year, month, report["report"], report["directory"], report_id, base_dir
            )
        )
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


def download_mmsdm(start, end, report_id, base_dir):
    urls = make_many_report_urls(start, end, report_id, base_dir)

    output = []
    for url in urls:
        clean_fi = url.home / "clean.parquet"
        if clean_fi.exists():
            print(f" {clean_fi} exists - not redownloading")
            data = pd.read_parquet(clean_fi)
        else:
            print(f" {clean_fi} does not exist - downloading")
            zf = download_zipfile_from_url(url)
            unzip(zf)

            data = load_unzipped_report(url, zf)

            #  unpacking the report dict - must be better way...
            report = reports[report_id]
            timestamp_col = report["interval-col"]

            data = make_dt_cols(data, report["dt-cols"])

            #  accounting for AEMO stamping intervals at the end
            #  usually intervals are stamped at the start
            data = add_interval_cols(data, timestamp_col, report["freq"])

            #  could check by assert difference == freq
            print(f" saving csv and parquet to {url.home}/clean.{{csv,parquet}}")
            data.to_csv(clean_fi.with_suffix(".csv"))
            data.to_parquet(clean_fi.with_suffix(".parquet"))

        output.append(data)

    return pd.concat(output, axis=0)
