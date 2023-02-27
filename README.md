# nem-data

A simple & opinionated Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).  It features:

- access to the NEMDE dataset as well as the predispatch, unit-scada, trading-price, demand and interconnectors tables from MMSDM,
- a cache to not re-download data that already exists in `~/nem-data/data`,
- adds `interval-start` and `interval-end` columns.

It is designed for use by researchers & data scientists - this tool supports my personal research work.  It is not designed for production use - see [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) for a production grade package.

See [A Hackers Guide to AEMO & NEM Data](https://adgefficiency.com/hackers-aemo/) for more context on the data provided by AEMO.


## Setup

```bash
$ pip install nemdata
```


## Use

### CLI

```shell-session
$ nemdata --help
Usage: nemdata [OPTIONS]

  Downloads NEM data from AEMO.

Options:
  -t, --table TEXT          Available tables: nemde, dispatch-price,
                            predispatch, unit-scada, trading-price, demand,
                            interconnectors.
  -s, --start TEXT          Start date (YYYY-MM or YYYY-MM-DD for NEMDE).
  -e, --end TEXT            End date (incusive) (YYYY-MM or YYYY-MM-DD for
                            NEMDE).
  --dry-run / --no-dry-run  Whether to save downloaded data to disk.
  --help                    Show this message and exit.
```

Download NEMDE data for the first three days in January 2018:

```shell-session
$ nemdata -t nemde --start 2018-01-01 --end 2018-01-03
```

Download trading price data from MMSDM for January to March 2018:

```shell-session
$ nemdata -t trading-price -s 2018-01 -e 2018-03
```

### Python

Download trading price data from MMSDM for January to Feburary 2020:

```python
import nemdata

data = nemdata.download(start="2020-01", end="2020-02", table="trading-price")
```

Load this data back into a pandas DataFrame:

```python
data = nemdata.load()['trading-price']
```

At this point, `data` will have the trading price for all regions.


## Data

Downloaded into into `$HOME/nem-data/data/`:

```shell-session
$ nemdata -t trading-price -s 2020-01 -e 2020-02
$ tree ~/nem-data
/Users/adam/nem-data
└── data
    └── trading-price
        ├── 2020-01
        │   ├── PUBLIC_DVD_TRADINGPRICE_202001010000.CSV
        │   ├── clean.csv
        │   ├── clean.parquet
        │   └── raw.zip
        └── 2020-02
            ├── PUBLIC_DVD_TRADINGPRICE_202002010000.CSV
            ├── clean.csv
            ├── clean.parquet
            └── raw.zip
```

A few things happen during data processing:

- rows of the raw CSV are removed to create a rectangular, single table CSV,
- `interval-start` and `interval-end` timezone aware datetime columns are added,
- when using `nemdata.loader.loader` for `trading-price`, all data is resampled to a 5 minute frequency (both before and after the 30 to 5 minute settlement interval change).
