import os

from nemdata.use_cases import main

#  this goes into database???
class Files:
    def __init__(self, name):
        self.setup(name)

    def setup(self, name):
        self.folder = os.path.join(
            os.environ['HOME'],
            'nem-data',
            name
        )
        os.makedirs(self.folder, exist_ok=True)

    def insert(self, table, data):
        pass

def test_system():
    db = Files('test')
    main('trading', '2018-01', '2018-02', db)
