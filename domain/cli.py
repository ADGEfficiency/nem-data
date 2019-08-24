from databases import MemoryDatabase
from use_cases import get_generators

#  initialize the database
db = MemoryDatabase([])
#  initialize & run the use case (can be separated into init & run)
uc = get_generators(db)

print(uc)
