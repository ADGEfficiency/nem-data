import os

from nemdata.use_cases import main
from nemdata.databases import Files


def test_system():
    db = Files('test')
    main('trading', '2018-01', '2018-02', db)

    db = Files('test')
    main('nemde', '2018-01', '2018-02', db)
