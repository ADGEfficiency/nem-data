# nem-data

A simple Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

The tool aims to supply the most useful data only - see [A hackers guide to AEMO & NEM data](https://adgefficiency.com/hackers-aemo/) for more on the data provided by AEMO about the NEM.

It is designed to access historical data, for use by researchers & data scientists.


## Setup

Install as editable package:

```bash
$ make setup
```


## Use

Data is downloaded into into `$HOME/nem-data/data/`:

To download NEMDE data:

```bash
$ nemdata --report nemde --start 2018-01 --end 2018-03

$ nemdata --report trading-price --start 2018-01 --end 2018-03
```

Also support the following from MMSDM:

```python
reports = {
    'trading-price': 'TRADINGPRICE',
    'unit-scada': 'UNIT_SCADA',
    'dispatch-price': 'DISPATCHPRICE',
    'demand': 'DISPATCHREGIONSUM',
    'interconnectors': 'DISPATCHINTERCONNECTORRES'
}
```

For example, to download the interconnector data into `$HOME/nem-data/interconnectors`:

```bash
$ nemdata --reports interconnectors --start 2018-01 --end 2018-03
```

Multiple reports can be downloaded at once:

```bash
$ nemdata -r interconnectors -r nemde --start 2018-01 --end 2018-03
```
