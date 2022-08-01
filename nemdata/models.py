from pydantic import BaseModel
from typing import Type, Union
from pathlib import Path


class UOW(BaseModel):
    name: str
    table: str

    url: str
    year: int
    month: str

    fi: str
    raw_fi: Path
    raw_zip: Path
    processed_fi: Path
