import json

from domain import Generator
from seralizers import JSONEncoder
from databases import MemoryDatabase


def test_generator_from_dict():
    gen = Generator.from_dict({
        'duid': 'A',
        'intensity': 0.9
    })

    assert gen.duid == 'A'
    assert gen.intensity == 0.9


def test_seralize_generator():
    gen = Generator(
            duid='A',
            intensity=0.9
    )

    expected = """{"duid": "A", "intensity": 0.9}"""

    json_gen = json.dumps(gen, cls=JSONEncoder)

    assert json.loads(json_gen) == json.loads(expected)


def test_memory_get_generators():
    generators = [
        {'duid': 'A', 'intensity': 0.9},
        {'duid': 'B', 'intensity': 0.6},
        {'duid': 'C', 'intensity': 1.1},
    ]

    db = MemoryDatabase(generators)
    assert db.get_generators() == [Generator.from_dict(d) for d in generators]
