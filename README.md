# nem-data

A simple & opinionated Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

It is designed for use by researchers & data scientists - this tool supports my personal research work.  It is not designed for production use - see [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) for a production grade package.

See [A hackers guide to AEMO & NEM data](https://adgefficiency.com/hackers-aemo/) for more on context the data provided by AEMO.


## Setup

Install as editable package:

```bash
$ make setup
```


## Use

```shell-session
$ nemdata --help
Usage: nemdata [OPTIONS]

  nem-data is a tool to access NEM data

Options:
  -s, --start TEXT    start date (YYYY-MM)
  -e, --end TEXT      end date (incusive) (YYYY-MM)
  -r, --report TEXT  nemde, predispatch, unit-scada, trading-price
  --help              Show this message and exit.
```


To download NEMDE data:

```bash
$ nemdata -r nemde --start 2018-01 --end 2018-03
```

To download trading price data:

```python
$ nemdata -r trading-price -s 2018-01 -e 2018-03
```

Support the following datasets from MMSDM:

```python
reports = {
    'trading-price': 'TRADINGPRICE',
    'unit-scada': 'UNIT_SCADA',
    'predispatch': "PREDISPATCHPRICE"
}
```


## Output Data

Data is downloaded into into `$HOME/nem-data/data/`:

```shell-session
$ nemdata -r trading-price -s 2020-01 -e 2020-02
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

4 directories, 8 files
```

A few things happen during data processing:

- the top & bottom rows of the raw CSV are removed,
- `interval-start` and `interval-end` columns are added,
- for `trading-price`, all data is resampled to a 5 minute frequency (both before and after the 30 to 5 minute settlement interval change).
