from fastapi import APIRouter
from src.experiments.MontyHall.schemas import (
    MontyHallBatchResponse,
    MontyHallBatchRequest
)
from src.experiments.MontyHall.logic.engine import Simulate

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


@router.post("/simulate", response_model=MontyHallBatchResponse)
def start_simulate(data: MontyHallBatchRequest):
    simulate = Simulate()
    results = []

    for elem_data in data.simulations:
        count_prizes = elem_data.count_prizes
        count_doors = elem_data.count_doors
        closed_doors = elem_data.closed_doors

        result = simulate.start_simulate(count_prizes=count_prizes,
                                         count_doors=count_doors,
                                         closed_doors=closed_doors)
        results.append(result)
    return MontyHallBatchResponse(batch_results=results)
