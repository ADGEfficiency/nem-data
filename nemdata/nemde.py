import os

import pandas as pd

from nemdata.interfaces import scrape_url, unzip_file


def form_nemde_url(year, month, day):
    month = str(month).zfill(2)
    day = str(day).zfill(2)
    return 'http://www.nemweb.com.au/Data_Archive/Wholesale_Electricity/NEMDE/{0}/NEMDE_{0}_{1}/NEMDE_Market_Data/NEMDE_Files/NemPriceSetter_{0}{1}{2}_xml.zip'.format(year, month, day)


def main(start, end, db=None):
    months = pd.date_range(start=start, end=end, freq='D')
    for year, month, day in zip(months.year, months.month, months.day):
        month = str(month).zfill(2)
        day = str(day).zfill(2)
        url = form_nemde_url(year, month, day)

        z_file = os.path.join(db.root, '{}-{}-{}.zip'.format(year, month, day))
        if os.path.isfile(z_file):
            print('not downloading {}'.format(url))

        else:
            print('downloading {}'.format(url))
            f = scrape_url(url, z_file) # TODO return the file?
            unzip_file(z_file, db.root)
        print(' ')
