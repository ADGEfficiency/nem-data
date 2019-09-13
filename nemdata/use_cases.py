import os

from nemdata.mmsdm import main as mmsdm
from nemdata.nemde import main as nemde


def main(report, start, end, db):
    reports = [
        ('trading', 'TRADINGPRICE'),
        ('unit-scada', 'UNIT_SCADA'),
        ('dispatch', 'DISPATCHPRICE'),
        ('demand', 'DISPATCHREGIONSUM'),
        ('interconnectors', 'DISPATCHINTERCONNECTORRES')
    ]

    if report == 'nemde':
        nemde(start, end, db)
    else:
        report = reports[-1][1]
        mmsdm(report, start, end, db)
