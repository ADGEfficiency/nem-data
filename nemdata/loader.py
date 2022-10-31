import pandas as pd
from nemdata.config import HOME


def concat(report_id, pkg):
    data = [p for p in report_id.glob("**/clean.parquet")]
    data = [pd.read_parquet(p) for p in data]
    pkg[report_id.name] = pd.concat(data, axis=0)
    return pkg


def concat_trading_price(report_id, pkg):
    raise NotImplementedError('todo')


def loader():
    pkg = {}
    report_ids = [p for p in HOME.iterdir() if p.is_dir()]
    print(f"found {report_ids}")

    #  default to loading everything
    for report_id in report_ids:

        if report_id == 'trading-price':
            pkg = concat_trading_price(report_id, pkg)
        else:
            pkg = concat(report_id, pkg)

    return pkg

