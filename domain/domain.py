class Generator:
    def __init__(self, duid, intensity):
        self.duid = duid
        self.intensity = intensity

    @classmethod
    def from_dict(cls, data):
        return cls(
            duid=data['duid'],
            intensity=data['intensity']
        )

    def to_dict(self):
        return {
            'duid': self.duid,
            'intensity': self.intensity
        }

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()
