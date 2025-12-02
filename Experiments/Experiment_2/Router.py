from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/experiment_2",
    tags=["Experiment_2"]
)


@router.get("/")
def info():
    return {"experiment": "Experiment_2"}
