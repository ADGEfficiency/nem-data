import os

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file, download_report


def form_nemde_url(year, month, day):
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/{0}/NEMDE_{0}_{1}/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_{0}{1}{2}_xml.zip'.format(year, month, day)


def main(start, end, db):
    months = pd.date_range(start=start, end=end, freq='D')
    for year, month, day in zip(months.year, months.month, months.day):
        month = str(month).zfill(2)
        day = str(day).zfill(2)

        url = form_nemde_url(year, month, day)
        fldr = db.root
        z_file = os.path.join(db.root, '{}-{}-{}.zip'.format(year, month, day))

        download_report(fldr, z_file, url)
