## Usage

```bash
python nemdata/cli.py --report interconnector --start 2018-01 --end 2018-03

python nemdata/cli.py --report nemde
```

## Setup

```bash
python setup.py install
```

## Who is `nem-data` for

Researchers & data scientists who want access to the most useful data supplied by AEMO for the NEM.

##  Philosophy

Only download what is needed
- not the entire mmsdm, just the report
- don't download twice

Clean architecture - use cases, interfaces
