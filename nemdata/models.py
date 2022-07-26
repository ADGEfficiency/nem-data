from pydantic import BaseModel
from typing import Type, Union
from pathlib import Path


class UOW(BaseModel):
    name: str
    url: str
    year: int
    month: str
    csv: str

    raw_fi: Path
