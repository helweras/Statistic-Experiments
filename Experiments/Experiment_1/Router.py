from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/experiment_1",
    tags=["Experiment_1"]
)


@router.get("/")
def info():
    return {"experiment": "Experiment_1"}
