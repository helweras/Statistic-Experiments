from fastapi import APIRouter
from Models.Monty_Hall import MontyHallData
from Experiments.MontyHall.Logic import start_experiment, valid_input_data

router = APIRouter(
    prefix='/monty_hall',
    tags=["Monty Hall"]
)

rules = """Запас дверей: Призов должно быть хотя бы на два меньше, чем всего дверей.
✅ Правильно: 1 приз и 3 двери (остается место для маневра).
❌ Ошибка: 2 приза и 3 двери (слишком много призов, не выполняется count_prize <= count_door - 2).
Действия ведущего: Ведущий должен оставить закрытыми столько дверей, чтобы там поместились все призы, но при этом он не может оставить закрытыми вообще все двери.
✅ Правильно: 1 приз, 10 дверей, ведущий оставил закрытыми 2 двери (игрок может сменить выбор).
❌ Ошибка: 1 приз, 3 двери, ведущий оставил закрытыми 3 двери (он ни одной не открыл, условие count_door - 1 > closed_door нарушено).
Реальность чисел: Нельзя использовать ноль или отрицательные числа.
✅ Правильно: 1, 3, 1.
"""


@router.get("/info")
def info():
    return {
        "status": "Good",
        "rules": rules
    }


@router.post("/simulate")
def start_simulate(data: MontyHallData):
    count_prize = data.count_prize
    count_door = data.count_doors
    closed_doors = data.closed_doors
    if valid_input_data(count_prize=count_prize, count_door=count_door, closed_door=closed_doors):

        result = start_experiment(count_prize=count_prize, count_door=count_door, closed_door=closed_doors)
        return {
            "status": "Good",
            "data": result
        }
    else:
        return {
            "status": "Bad",
            "error": "400",
            "name_error": "bad request",
            "msg": "Данные не прошли валидацию"
        }
