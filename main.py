from fastapi import FastAPI
from Experiments.MontyHall import Router as Monty

app = FastAPI()
app.include_router(Monty.router)


# uvicorn main:app --reload - для запуска сервера

@app.get("/")
def start():
    return {
        "status": "Good",
        "experiments":
            [{
                "name": "Monty_Hall",
                "name_on_page": "Парадокс Монти-Холла",
                "uuid": 123345,
                "description": "anything"
            },
                {
                    "name": "Experiment_1",
                    "name_on_page": None,
                    "uuid": 123345,
                    "description": "anything"
                },
                {
                    "name": "Playground Paradox",
                    "name_on_page": "Институт парадоксов родства",
                    "uuid": 123345,
                    "description": "anything"
                }]

    }


if __name__ == '__main__':
    pass
