from domain import Generator


class MemoryDatabase:
    def __init__(self, data):
        self.data = data

    def get_generators(self):
        return [Generator.from_dict(d) for d in self.data]

