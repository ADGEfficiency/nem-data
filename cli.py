# from databases import MemoryDatabase
from use_cases import download_reports

#  initialize the database
# db = MemoryDatabase([])

import argparse


def setup_parser():
    """ cil interface """
    parser = argparse.ArgumentParser(description='start and end months')
    parser.add_argument('--start', type=str, default='2018-01', nargs='?')
    parser.add_argument('--end', type=str, default='2019-01', nargs='?')
    parser.add_argument('--report', type=str, default='all', nargs='?')
    return parser.parse_args()



reports = [
    ('trading', 'TRADINGPRICE'),
    ('unit-scada', 'UNIT_SCADA'),
    ('dispatch', 'DISPATCHPRICE'),
    ('demand', 'DISPATCHREGIONSUM'),
    ('interconnectors', 'DISPATCHINTERCONNECTORRES')
]
args = setup_parser()
if args.report == 'all':
    report = reports[-1][1]
#  initialize & run the use case (can be separated into init & run)
uc = download_reports(report, args.start, args.end, db=None)

print(uc)

# todo check if already there
