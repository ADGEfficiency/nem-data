import os

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file, download_report

#  add in the frequency of the datetime index
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


def clean_report(input_file, output_file, freq):
    #  remove first row via skiprows
    raw = pd.read_csv(input_file, skiprows=1)
    #  remove last row via iloc
    raw = raw.iloc[:-1, :]

    settlement_date = pd.to_datetime(raw['SETTLEMENTDATE'])
    raw.loc[:, 'interval-end'] = settlement_date
    raw.loc[:, 'interval-start'] = settlement_date - pd.Timedelta(freq)

    if 'RRP' in raw.columns:
        raw.loc[:, 'trading-price'] = raw['RRP']

    raw.to_csv(output_file, index=False)


def main(report, start, end, db):
    report = reports[report]

    half_hour_intervals = ['trading-price']
    freq = '5T'
    if report in half_hour_intervals:
        freq = '30T'

    months = pd.date_range(start=start, end=end, freq='M')
    for year, month in zip(months.year, months.month):
        month = str(month).zfill(2)

        url = form_report_url(year, month, report)
        fldr = db.setup('{}-{}'.format(year, month))
        z_file = os.path.join(fldr, f'{report}.zip')
        download_report(fldr, z_file, url)

        name, date = fldr.split('/')[-2], fldr.split('/')[-1]
        clean_report(
            input_file=os.path.join(fldr, os.path.splitext(url.split('/')[-1])[0]+'.CSV'),
            output_file=os.path.join(fldr, f'clean.csv'),
            freq=freq
        )
