# nem-data

A simple command line tool to access Australian National Energy Market (NEM) data provided by the Australian Energy Market Operator (AEMO).

For more background on this project read the [project page on Climate Code]().

## Setup

```bash
python setup.py install
```

## Usage

To download the Downloads data into `$HOME/nem-data/interconnector`:

```bash
nem --reports interconnector --start 2018-01 --end 2018-03
```

Downloads data into `$HOME/nem-data/nemde`:

```bash
nem --reports nemde
```
