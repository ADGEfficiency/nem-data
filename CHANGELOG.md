0.3.2
- fix bug introduced in 0.3.1 where cache not used properly.

0.3.1
- add timezones to MMSDM and NEMDE data,
- added `make clean` to remove the data cache,
- added `nemdata.constants` for the NEM timezone,
- added graceful failure when data not available on MMSDM or NEMDE.

0.3.0
- introduce `nemdata.downloader`,
- rename `nemdata.loader.loader` to `nemdata.loader.load`,
- add tests for README Python code.

0.2.1 
- add `DISPATCHREGIONSUM` and `INTERCONNECTORRES` MMSDMTables,
- add `skip publish` to publish CI.

0.2.0
- breaking change moving from concept of `report` to concept of `table`,
- breaking CLI option change from `-r --report` to `-t` `--table`,
- added `--dry-run` to CLI,
- added changelog,
- add `pydantic`, `black` and `isort`,
- introduce `MMSDMTable` and `MMSDMFile`,
- add `make check`, `make lint` and `make static`,
- added static typing check to CI,
- added `frequency_minutes` as a column in `clean.parquet`.

0.1.4 - cleanup unused code.

0.1.3 - fix loader bug.

0.1.2 - missed version.

0.1.1 - add to pypi.
