import os


class Files:
    """Uses the filesystem"""

    def __init__(self, name):
        self.name = name
        self.root = os.path.join(os.path.expanduser("~"), "nem-data", self.name)
        os.makedirs(self.root, exist_ok=True)

    def setup(self, name):
        sub = os.path.join(self.root, name)
        os.makedirs(sub, exist_ok=True)
        return sub
