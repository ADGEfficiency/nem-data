import os

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file


reports = {
    'trading-price': 'TRADINGPRICE',
    'unit-scada': 'UNIT_SCADA',
    'dispatch-price': 'DISPATCHPRICE',
    'demand': 'DISPATCHREGIONSUM',
    'interconnectors': 'DISPATCHINTERCONNECTORRES'
}


def form_report_url(year, month, report):
    month = str(month).zfill(2)
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{0}/MMSDM_{0}_{1}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_{2}_{0}{1}010000.zip'.format(year, month, report)


def clean_report(input_file, output_file):
    #  remove first row via skiprows
    raw = pd.read_csv(input_file, skiprows=1)
    #  remove last row via iloc
    raw = raw.iloc[:-1, :]
    raw.to_csv(output_file, index=False)


def download_reports(report, start, end, db):
    months = pd.date_range(start=start, end=end, freq='M')
    for year, month in zip(months.year, months.month):
        month = str(month).zfill(2)
        url = form_report_url(year, month, report)

        sub_dir = db.setup('{}-{}'.format(year, month))
        z_file = os.path.join(sub_dir, '{}.zip'.format(report))
        if os.path.isfile(z_file):
            print('not downloading {}'.format(url))

        else:
            print('downloading {}'.format(url))
            f = scrape_url(url, z_file)
            unzip_file(z_file, sub_dir)

            clean_report(
                input_file=os.path.join(sub_dir, os.path.splitext(url.split('/')[-1])[0]+'.CSV'),
                output_file=os.path.join(sub_dir, 'clean.csv'.format(report))
            )
        print(' ')


def main(report, start, end, db):
    report = reports[report]
    download_reports(report, start, end, db)
