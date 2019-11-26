from nemdata.mmsdm import main as mmsdm
from nemdata.nemde import main as nemde


def main(report, start, end, db):
    if report == 'nemde':
        nemde(start, end, db)
    else:
        mmsdm(report, start, end, db)
