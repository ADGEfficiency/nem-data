import pandas as pd
from nemdata.config import HOME


def concat(report_id, pkg):
    data = [p for p in report_id.glob("**/clean.parquet")]
    data = [pd.read_parquet(p) for p in data]
    pkg[report_id.name] = pd.concat(data, axis=0)
    return pkg


def concat_trading_price(report_id, pkg):
    fis = [p for p in report_id.glob("**/clean.parquet")]
    datas = []
    for fi in fis:
        data = pd.read_parquet(fi)
        for region in data['REGIONID'].unique():
            raw = data[data['REGIONID'] == region]
            raw = raw.set_index('interval-start').sort_index()
            subset = raw.resample("5T").ffill()
            datas.append(subset)

    pkg[report_id.name] = pd.concat(datas).reset_index()
    return pkg


def loader(desired_reports = None):
    pkg = {}
    report_ids = [p for p in HOME.iterdir() if p.is_dir()]
    print(f"found {report_ids}")

    if desired_reports is not None:
        report_ids = [p for p in report_ids if p.name in desired_reports]
    print(f"loading {report_ids}")

    #  default to loading everything
    for report_id in report_ids:
        if report_id.name == 'trading-price':
            pkg = concat_trading_price(report_id, pkg)
        else:
            pkg = concat(report_id, pkg)

    return pkg

