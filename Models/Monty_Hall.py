from pydantic import BaseModel


class MontyHallData(BaseModel):
    count_prize: int = 1
    count_doors: int = 3
    closed_doors: int = 1
    iterable: int = 1000
