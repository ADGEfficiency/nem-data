import argparse
import os

from nemdata.databases import Files
from nemdata.use_cases import main as use_cases


def setup_parser():
    """ cil interface """
    parser = argparse.ArgumentParser(description='start and end months')
    parser.add_argument('--start', type=str, default='2018-01', nargs='?')
    parser.add_argument('--end', type=str, default='2019-01', nargs='?')
    parser.add_argument('--report', type=str, default='all', nargs='?')
    return parser.parse_args()


if __name__ == '__main__':
    args = setup_parser()
    print(args)

    start = args.start
    end = args.end
    report = args.report

    use_cases(report, start, end, Files(report))
