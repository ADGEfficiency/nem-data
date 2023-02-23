## Pull Requests

Prefix pull requests with one of `[TECH], [FEATURE], [BUG]`.

Include tests - especially if you are introducing code that is not covered by existing tests.

# Adding MMSDM Tables

1. Add `MMSDMTable` objects into `nemdata/mmsdm.py`,
2. Add the new table objects into `nemdata/downloader.py`,
3. Add tests for the uploading and downloading.

A good model for how to add MMSDM tables is [#25](https://github.com/ADGEfficiency/nem-data/pull/25).
