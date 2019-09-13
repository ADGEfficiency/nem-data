import os


class Files:
    def __init__(self, name):
        self.name = name

    def setup(self, name):
        self.folder = os.path.join(
            os.environ['HOME'],
            'nem-data',
            self.name,
            name
        )
        os.makedirs(self.folder, exist_ok=True)
