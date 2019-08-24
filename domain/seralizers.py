
import json

class JSONEncoder(json.JSONEncoder):
    def default(self, gen):
        return gen.to_dict()
