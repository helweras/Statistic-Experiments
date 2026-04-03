from pydantic import BaseModel


class BloodTilesData(BaseModel):
    weight: tuple
    value: int
    count_sim: int
    num_of_family: int
