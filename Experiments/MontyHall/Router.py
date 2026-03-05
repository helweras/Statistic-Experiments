from fastapi import APIRouter
from Models.Monty_Hall import MontyHallData
from Experiments.MontyHall.Logic import start_experiment, valid_input_data

router = APIRouter(
    prefix='/monty_hall',
    tags=["Monty Hall"]
)

rules = """
### 🚪 Правила настройки игры

---

#### 1. Свободное место
Призов должно быть как минимум **на два меньше**, чем всех дверей. Это нужно, чтобы у игрока всегда был выбор.
* 🟢 **Хорошо:** 1 приз и 3 двери — есть место для маневра.
* 🔴 **Плохо:** 2 приза и 3 двери — слишком много призов, интрига исчезает.

#### 2. Роль ведущего
Ведущий обязан открыть хотя бы одну дверь, но оставить закрытыми столько, чтобы там поместились все призы.
* 🟢 **Хорошо:** 10 дверей, закрыто 2 — вы можете сменить выбор и рискнуть.
* 🔴 **Плохо:** Ведущий не открыл ни одной двери — игра не началась.

#### 3. Только реальные числа
Используйте только целые положительные числа. Никаких нулей или отрицательных значений.
* 🟢 **Пример:** 1 приз, 3 двери, 1 закрытая.

---
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
