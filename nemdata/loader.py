from pathlib import Path

from rich import print
import pandas as pd

from nemdata import database, tables


def resample_pre_settlement_transition(raw: pd.DataFrame) -> pd.DataFrame:
    #  get everything before the transition from 30 min to 5 min settlement
    dupes = raw.index.duplicated()
    before = raw[~dupes]
    raw = raw[raw.index < settlement_transition_date]
    #  resample to 5 min
    #  should probably check this though???? TODO
    before = before.resample("5T").ffill()

    #  get everything after & join
    data = [before, raw[raw.index >= settlement_transition_date]]
    data = pd.concat(data, axis=0)
    return data


def loader():
    load = {}
    #  do each dataset / table separately
    for table_dir in [p for p in database.homebase.iterdir()]:
        table = tables.get_table(table_dir.name)
        print(table.name)

        #  get all data for this table
        data = [p for p in table_dir.glob("**/clean.parquet") if p.is_file()]

        #  think you could walrus here
        if data:
            print(f" found {len(data)} clean.parquet")
            data = [pd.read_parquet(p) for p in data]
            data = pd.concat(data, axis=0)
            load[table.name] = data

        else:
            print("no data")
    return load
