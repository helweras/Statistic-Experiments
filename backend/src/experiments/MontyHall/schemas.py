from pydantic import BaseModel, model_validator, Field
from typing import Dict



class MontyHallDataRequest(BaseModel):
    count_prize: int = Field(
        default=1,
        gt=0,
        description="Количество призов (выигрышных дверей) в игре"
    )

    count_doors: int = Field(
        default=3,
        gt=1,
        le=100,
        description="Общее количество дверей в симуляции"
    )

    closed_doors: int = Field(
        default=1,
        gt=0,
        description="Количество дверей, которые ведущий оставляет закрытыми"
    )

    iterable: int = Field(
        default=1000,
        gt=100,
        le=1000,
        description="Количество итераций (повторений) эксперимента для статистики"
    )

    @model_validator(mode="after")
    def valid_input_data(self) -> "MontyHallDataRequest":

        # Извлекаем данные для удобства
        prizes = self.count_prize
        doors = self.count_doors
        closed = self.closed_doors

        if prizes <= 0 or doors <= 0 or closed <= 0:
            raise ValueError("Все значения (призы, двери, закрытые двери) должны быть больше 0")

        if prizes > (doors - 2):
            raise ValueError(
                f"Количество призов ({prizes}) слишком велико для такого количества дверей ({doors}). "
                f"Призов должно быть не больше, чем дверей минус 2 (максимум {doors - 2})"
            )

        if not (doors - 1 > closed >= prizes):
            raise ValueError(
                f"Некорректное количество закрытых дверей ведущего ({closed}). "
                f"Оно должно быть строго меньше общего числа дверей без одной ({doors - 1}) "
                f"и больше либо равно числу призов ({prizes})"
            )

        return self


class MontyHallDataResponse(BaseModel):
    data_experiments: Dict[str, float]
