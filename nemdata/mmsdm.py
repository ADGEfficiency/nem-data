import os

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file


def form_report_url(year, month, report):
    month = str(month).zfill(2)
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{0}/MMSDM_{0}_{1}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_{2}_{0}{1}010000.zip'.format(year, month, report)


def clean_report(input_file, output_file):
    #  remove first row via skiprows
    raw = pd.read_csv(input_file, skiprows=1)
    #  remove last row via iloc
    raw = raw.iloc[:-1, :]
    raw.to_csv(output_file)


def download_reports(report, start, end, db=None):
    months = pd.date_range(start=start, end=end, freq='M')

    for year, month in zip(months.year, months.month):
        url = form_report_url(year, month, report)

        db.setup('{}-{}'.format(year, month))

        folder = os.path.join(db.folder, '{}-{}'.format(year, month))
        os.makedirs(folder, exist_ok=True)
        z_file = os.path.join(folder, '{}.zip'.format(report))

        print(url)

        if os.path.isfile(z_file):
            print('not downloading {}'.format(url))

        else:
            print('downloading {}'.format(url))
            f = scrape_url(url, z_file)
            unzip_file(z_file, folder)

            clean_report(
                input_file=os.path.join(folder, os.path.splitext(url.split('/')[-1])[0]+'.CSV'),
                output_file=os.path.join(folder, '{}.csv'.format(report))
            )


def main(report, start, end, db):
    reports = [
        ('trading', 'TRADINGPRICE'),
        ('unit-scada', 'UNIT_SCADA'),
        ('dispatch', 'DISPATCHPRICE'),
        ('demand', 'DISPATCHREGIONSUM'),
        ('interconnectors', 'DISPATCHINTERCONNECTORRES')
    ]

    report = reports[-1][1]

    uc = download_reports(report, start, end, db)
