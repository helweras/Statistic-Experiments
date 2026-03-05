from fastapi import APIRouter
from Models.Monty_Hall import MontyHallData
from Experiments.MontyHall.Logic import start_experiment, valid_input_data

router = APIRouter(
    prefix='/monty_hall',
    tags=["Monty Hall"]
)

rules = """
### 🚪 Правила Парадокса Монти Холла

**1. Запас дверей**
Призов должно быть хотя бы на два меньше, чем всего дверей.
* ✅ **Правильно:** 1 приз и 3 двери (есть место для маневра).
* ❌ **Ошибка:** 2 приза и 3 двери (не выполняется `count_prize ≤ count_door - 2`).

---

**2. Действия ведущего**
Ведущий оставляет закрытыми столько дверей, чтобы там поместились все призы, но не может оставить закрытыми все двери.
* ✅ **Правильно:** 1 приз, 10 дверей, закрыто 2 (игрок может сменить выбор).
* ❌ **Ошибка:** 1 приз, 3 двери, закрыто 3 (нарушено `count_door - 1 > closed_door`).
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
