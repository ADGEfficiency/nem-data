# nem-data

A simple & opinionated Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

It is designed for use by researchers & data scientists - this tool supports my personal research work.  It is not designed for production use - see [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) for a production grade package.

See [A Hackers Guide to AEMO & NEM Data](https://adgefficiency.com/hackers-aemo/) for more on context the data provided by AEMO.


## Setup

```bash
$ make setup
```


## Use

```shell-session
$ nemdata --help
Usage: nemdata [OPTIONS]

  nemdata is a tool to access NEM data from AEMO.

Options:
  -t, --table TEXT          nemde, predispatch, unit-scada, trading-price
  -s, --start TEXT          start date (YYYY-MM)
  -e, --end TEXT            end date (incusive) (YYYY-MM)
  --dry-run / --no-dry-run  whether to save downloaded data to disk
  --help                    Show this message and exit.
```

`nem-data` supports downloading the following data - `nemde`, `predispatch`, `unit-scada` and `trading-price`.

To download NEMDE data:

```bash
$ nemdata -t nemde --start 2018-01 --end 2018-03
```

To download trading price data:

```python
$ nemdata -t trading-price -s 2018-01 -e 2018-03
```


## Output Data

Data is downloaded into into `$HOME/nem-data/data/`:

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

4 directories, 8 files
```

A few things happen during data processing:

- the top & bottom rows of the raw CSV are removed,
- `interval-start` and `interval-end` columns are added,
- when using `nemdata.loader.loader` for the `trading-price`, all data is resampled to a 5 minute frequency (both before and after the 30 to 5 minute settlement interval change).
