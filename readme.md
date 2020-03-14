# nem-data

A simple Python command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

The tool aims to supply the most useful data only - see [A hackers guide to AEMO & NEM data](https://adgefficiency.com/hackers-aemo/) for more on the data provided by AEMO about the NEM.

It is designed to access historical data, for use by researchers & data scientists.

## Setup

```bash
python setup.py install
```

## Usage

To download the interconnector data into `$HOME/nem-data/interconnector`:

```bash
nem --reports interconnector --start 2018-01 --end 2018-03
```

Currently support the NEMDE data, plus the following from MMSDM:
```python
reports = {
    'trading-price': 'TRADINGPRICE',
    'unit-scada': 'UNIT_SCADA',
    'dispatch-price': 'DISPATCHPRICE',
    'demand': 'DISPATCHREGIONSUM',
    'interconnectors': 'DISPATCHINTERCONNECTORRES'
}
```

You can also

All data is downloadede into Downloads data into `$HOME/nem-data`.
