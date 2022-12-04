# nem-data

A simple Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

It is designed to access historical data, for use by researchers & data scientists.  This tool supports my personal research work.  It is not designed for production use - see [NEMOSIS](https://github.com/UNSW-CEEM/NEMOSIS) for a production grade package.

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

Data is downloaded into into `$HOME/nem-data/data/`:

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

