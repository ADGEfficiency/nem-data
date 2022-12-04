import os
from pathlib import Path

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file
from nemdata.utils import URL, add_interval_cols, download_zipfile_from_url, unzip


def make_nemde_url(year, month, day, base_dir):
    month = str(month).zfill(2)
    day = str(day).zfill(2)

    home = base_dir / "nemde" / f"{year}-{month}-{day}"
    home.mkdir(exist_ok=True, parents=True)

    return URL(
        url=f"http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/{year}/NEMDE_{year}_{month}/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_{year}{month}{day}_xml.zip",
        year=year,
        month=month,
        report="nemde",
        csv=None,
        xml=f"NemPriceSetter_{year}{month}{day}.xml",
        home=home,
    )


def make_many_nemde_urls(start, end, base_dir):
    urls = []
    months = pd.date_range(start=start, end=end, freq="D")
    for year, month, day in zip(months.year, months.month, months.day):
        urls.append(make_nemde_url(year, month, day, base_dir))
    return urls


def find_xmls(path):
    fis = [p for p in Path(path).iterdir() if p.suffix == ".xml"]
    return [pd.read_xml(f) for f in fis]


def download_nemde(start, end, report_id, base_dir):
    assert report_id == "nemde"
    urls = make_many_nemde_urls(start, end, base_dir)
    output = []
    for url in urls:
        zf = download_zipfile_from_url(url)
        unzip(zf)
        xmls = find_xmls(url.home)

        clean = pd.concat(xmls, axis=0)

        #  get problems with a value of '5' without the cast to float
        clean["BandNo"] = clean["BandNo"].astype(float)

        #  accounting for AEMO stamping intervals at the end
        #  usually intervals are stamped at the start
        clean["PeriodID"] = pd.to_datetime(clean["PeriodID"]).dt.tz_localize(None)
        clean = add_interval_cols(clean, "PeriodID", "5T")

        print(f" saving csv and parquet to {url.home}/clean")
        clean.to_csv(Path(url.home) / "clean.csv")
        clean.to_parquet(Path(url.home) / "clean.parquet")
