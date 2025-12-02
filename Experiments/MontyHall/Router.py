from fastapi import APIRouter
from Models.Monty_Hall import MontyHallData
from Experiments.MontyHall.Logic import start_experiment, valid_input_data

router = APIRouter(
    prefix='/monty_hall',
    tags=["Monty Hall"]
)


@router.get("/")
def info():
    return {
        "status": "Good",
        "base_data": {
            "doors": 3,
            "prize": 1,
            "close_doors": 2
        },
        "rules": "some rules"
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
