import os

import pandas as pd

from interfaces import scrape_url, unzip_file


def form_report_url(year, month, report):
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{0}/MMSDM_{0}_{1}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_{2}_{0}{1}010000.zip'.format(year, month, report)


def form_mmsdm_url(year, month):
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{0}/MMSDM_{0}_{1}.zip'.format(year, month)



def clean_report(input_file, output_file):
    #  remove first row via skiprows
    raw = pd.read_csv(input_file, skiprows=1)
    #  remove last row via iloc
    raw = raw.iloc[:-1, :]
    raw.to_csv(output_file)


def download_reports(report, start, end, db=None):
    months = pd.date_range(start=start, end=end, freq='M')

    for year, month in zip(months.year, months.month):
        month = str(month).zfill(2)
        url = form_report_url(year, month, report)

        folder = os.path.join(os.environ['HOME'], 'nem-data', 'single-reports', '{}-{}'.format(year, month))
        os.makedirs(folder, exist_ok=True)
        z_file = os.path.join(folder, '{}.zip'.format(report))

        print(url)

        scrape_url(url, z_file)

        unzip_file(z_file, folder)

        clean_report(
            os.path.join(
                folder,
                os.path.splitext(url.split('/')[-1])[0]+'.CSV'
            ),
            os.path.join(folder, '{}.csv'.format(report))
        )


def download_mmsdm(report, start, end, db=None):
    report = 'mmsdm'
    months = pd.date_range(start=args.start, end=args.end, freq='M')

    for year, month in zip(months.year, months.month):
        month = str(month).zfill(2)
        url = form_mmsdm_url(year, month)
        print(url)

        folder = os.path.join(os.environ['HOME'], 'nem-data', 'raw-mmsdm', '{}-{}'.format(year, month))
        os.makedirs(folder, exist_ok=True)
        z_file = os.path.join(folder, '{}.zip'.format(report))

        print(url)

        scrape_url(url, z_file)

        unzip_file(z_file, folder)
